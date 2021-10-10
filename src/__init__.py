import config
import src.views

from datetime import timezone, timedelta

from flask import Flask
from linebot import LineBotApi, WebhookHandler
from linebot.models import StickerSendMessage
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


# viewsで使いまわすやつ
room_names = [
    '学習席（有線LAN有）',
    '学習席',
    '研究個室',
    'インターネット・DB席',
    'グループ学習室',
    'ティーンズ学習室'
]


# メッセージ以外を受信した時に返すスタンプ群
sticker_messages = [
    StickerSendMessage(package_id=11537, sticker_id=52002753),
    StickerSendMessage(package_id=11537, sticker_id=52002739),
    StickerSendMessage(package_id=11537, sticker_id=52002757),
    StickerSendMessage(package_id=11539, sticker_id=52114110),
    StickerSendMessage(package_id=11539, sticker_id=52114121),
]

# 日本標準時
jst = timezone(timedelta(hours=+9), 'JST')


# Including other scripts
import src.views