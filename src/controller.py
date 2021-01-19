import re
from random import randint
from flask import request, abort
from linebot.models import (
    MessageEvent, TextSendMessage, StickerSendMessage,
    TextMessage, ImageMessage, VideoMessage, AudioMessage,
    LocationMessage, StickerMessage, FileMessage
)
from linebot.exceptions import InvalidSignatureError
from src import app, handler, line
from src.views import (
    crete_seats_info_message, create_reserve_notice_message,
    create_new_reserve_notice_message, create_usage_message
)


rooms = [
    '学習席（有線LAN有）',
    '学習席',
    '研究個室',
    'インターネット・DB席',
    'グループ学習室',
    'ティーンズ学習室'
]

sticker_messages = [
    StickerSendMessage(package_id=11537, sticker_id=52002753),
    StickerSendMessage(package_id=11537, sticker_id=52002739),
    StickerSendMessage(package_id=11537, sticker_id=52002757),
    StickerSendMessage(package_id=11539, sticker_id=52114110),
    StickerSendMessage(package_id=11539, sticker_id=52114121),
]


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

    # 空席情報
    if message in rooms:
        reply_message = crete_seats_info_message(message)

    # 空席通知予約
    elif message in [room + ' 予約' for room in rooms]:
        room_name = re.findall('(.+) 予約', message)[0]
        reply_message = create_reserve_notice_message(room_name, user_id)

    # 空席通知新規予約（既に予約済みだった場合新規の予約で上書きする）
    elif message in [room + ' 新規予約' for room in rooms]:
        room_name = re.findall('(.+) 新規予約', message)[0]
        reply_message = create_new_reserve_notice_message(room_name, user_id)

    elif message == '使い方':
        reply_message = create_usage_message()

    # 予期しないメッセージへの対応
    else:
        reply_message = create_usage_message()

    line.reply_message(event.reply_token, reply_message)


@handler.add(MessageEvent, message=[ImageMessage, VideoMessage, AudioMessage, LocationMessage, StickerMessage, FileMessage])
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
