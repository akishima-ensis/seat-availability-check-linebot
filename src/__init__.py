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
from linebot.models import StickerSendMessage
sticker_messages = [
    StickerSendMessage(package_id=11537, sticker_id=52002753),
    StickerSendMessage(package_id=11537, sticker_id=52002739),
    StickerSendMessage(package_id=11537, sticker_id=52002757),
    StickerSendMessage(package_id=11539, sticker_id=52114110),
    StickerSendMessage(package_id=11539, sticker_id=52114121),
]


# Including other scripts
import src.views