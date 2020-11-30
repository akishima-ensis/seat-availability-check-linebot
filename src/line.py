from src import app, handler, line, message
from flask import request, abort
from linebot.models import MessageEvent, TextMessage
from linebot.exceptions import InvalidSignatureError


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
    input_message = event.message.text
    reply_message = message.create(input_message)
    line.reply_message(event.reply_token, messages=reply_message)
