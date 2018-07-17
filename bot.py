from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)

line_bot_api = LineBotApi('37c611379f8a0aea23688980c721e611')
handler = WebhookHandler('o5dRyxRm6SSqpo7Xsz+PL1VNlGPR3Ba3xCXJv6E+QUibrPw7Ky39friRR2so1yLDePQXXCMUkwbbU67CscCq4oo28M9kvctIuWvW8dUjfo8oOBUKpJZrDJTHQZDNIUvikWh1F4c3jBzpxKMXtiaxTgdB04t89/1O/w1cDnyilFU=')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/hello line")
def hello_line():
    return "Hello Line"

@app.route("/webhook", methods=['GET','POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# @app.route("/webhook", methods=['GET', 'POST'])
# def webhook():
#     if request.method == 'POST':
#     return 'OK'    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
