import os
import firebase_admin
from firebase_admin import firestore
from datetime import datetime, timedelta, timezone
from flask import Flask, request, abort
from linebot.models import MessageEvent, TextMessage
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import flex_message_template


# firestoreの初期化（debug）
# from firebase_admin import credentials
# cred = credentials.Certificate('serviceAccountKey.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# firestoreの初期化（デバッグ時は以下2行をコメントアウト）
firebase_admin.initialize_app()
db = firestore.client()

# line-messaging-apiの初期化
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

app = Flask(__name__)

room_ids = {
    '学習席（有線LAN有）': 0,
    '学習席': 1,
    '研究個室': 2,
    'インターネット・DB席': 3,
    'グループ学習室': 4,
    'ティーンズ学習室': 5
}


def get_room_data():
    jst = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(jst)
    date = now.strftime('%Y%m%d')
    time = now.strftime('%H%M')

    doc_ref = db.collection('rooms').document(date)
    doc = doc_ref.get()

    rooms = []
    if doc.exists:
        rooms = doc.to_dict().get(time)
        if not rooms:
            rooms = doc.to_dict().get((now - timedelta(minutes=1)).strftime('%H%M'))

    return rooms


def create_message(message):
    if message in room_ids.keys():
        room_id = room_ids[message]
        room_data = get_room_data()
        if room_data:
            for room in room_data:
                if room.get('id') == room_id:
                    return flex_message_template.seats_info_message(room)
    else:
        return flex_message_template.failure_message_template()

    return flex_message_template.closing_day_message_template()


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    flex_message = create_message(message)
    line_bot_api.reply_message(event.reply_token, messages=flex_message)


if __name__ == '__main__':
    app.run(threaded=True)

    # debug
    # app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)