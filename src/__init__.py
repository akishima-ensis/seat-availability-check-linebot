import config

from datetime import timezone, timedelta

from flask import Flask
from linebot import LineBotApi, WebhookHandler
import firebase_admin
from firebase_admin import firestore


# setup for flask
app = Flask(__name__)
DEBUG = config.DEBUG
app.debug = DEBUG


# setup line-bot-sdk
LINE_CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET = config.LINE_CHANNEL_SECRET
line = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# setup for firebase
if DEBUG:
    from firebase_admin import credentials
    SERVICE_ACCOUNT_KEY = config.SERVICE_ACCOUNT_KEY
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()
db = firestore.client()


# 日本標準時
jst = timezone(timedelta(hours=+9), 'JST')

import src.views # noqa: F401, E402, E261
