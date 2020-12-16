import re
from flask import request, abort
from linebot.models import MessageEvent, TextMessage
from linebot.exceptions import InvalidSignatureError
from src import app, handler, line
from src.views import (
    crete_seats_info_message, create_reserve_notice_message,
    create_new_reserve_notice_message, create_failure_message
)


rooms = [
    '学習席（有線LAN有）',
    '学習席',
    '研究個室',
    'インターネット・DB席',
    'グループ学習室',
    'ティーンズ学習室'
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

    # 予期しないメッセージへの対応
    else:
        reply_message = create_failure_message()

    line.reply_message(event.reply_token, reply_message)
