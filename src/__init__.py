# setup for flask
import os
from flask import Flask

app = Flask(__name__)
app.debug = bool(os.environ.get('DEBUG'))


# setup line-bot-sdk
from linebot import LineBotApi, WebhookHandler

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
line = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# setup for firebase
import firebase_admin
from firebase_admin import credentials, firestore

cred_key = 'src/serviceAccountKey.json'
if os.path.exists(cred_key):
    cred = credentials.Certificate(cred_key)
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()
db = firestore.client()


# Including other scripts
import src.views