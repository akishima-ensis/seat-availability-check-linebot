from random import randint
from flask import request, abort
from linebot.models import (
    MessageEvent, TextSendMessage, TextMessage,
    ImageMessage, VideoMessage, AudioMessage,
    LocationMessage, StickerMessage, FileMessage
)
from linebot.exceptions import InvalidSignatureError

from src import app, handler, line, sticker_messages
from src.message import create_message


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
    user_id = event.source.user_id
    user_name = line.get_profile(user_id).display_name
    print(f"Received message: \"{message}\" from {user_name}")
    reply_content = create_message(user_id, message)
    line.reply_message(event.reply_token, reply_content)


@handler.add(MessageEvent, message=[
    ImageMessage, VideoMessage, AudioMessage,
    LocationMessage, StickerMessage, FileMessage])
def handle_other_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    user_name = line.get_profile(user_id).display_name
    print(f"Received message type: \"{message_type}\" from {user_name}")
    text = '送信されたメッセージタイプに対応していません。下記のリッチメニューから学習室名をタッチするか、学習室名を直接入力してください。'
    n = randint(0, len(sticker_messages)-1)
    line.reply_message(
        event.reply_token,
        messages=[
            TextSendMessage(text=text),
            sticker_messages[n]
        ]
    )
