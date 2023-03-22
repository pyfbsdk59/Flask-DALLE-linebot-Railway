# -*- coding: utf-8 -*-

import logging
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage
from linebot.models import TextSendMessage
import os

from flask import Flask, request



#################
import openai
	
openai.api_key = os.getenv("OPENAI_API_KEY")
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
#parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET")) 


	


class Dalle:  
    

    def __init__(self):
        
        self.image_url = ""



    def get_response(self, user_input):
        #import openai
        #openai.api_key = openai.api_key
        response = openai.Image.create(
            prompt = user_input,
                n=1,
            size="1024x1024"
            )
        self.image_url = response['data'][0]['url'].strip()
        print(self.image_url)


        
        return self.image_url
	



dalle = Dalle()

app = Flask(__name__)


@app.route("/")
def hello():
	return "Hello World from Flask in a uWSGI Nginx Docker container with \
	     Python 3.8 (from the example template)"
         
@app.route("/callback", methods=['POST'])
def callback():
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Get user's message
    user_message = event.message.text


    reply_dalle_url = dalle.get_response(user_message)
    
    
    #print(reply_pic)

    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url=reply_dalle_url, preview_image_url=reply_dalle_url)
    )





if __name__ == '__main__':
	    app.run(debug=True, port=os.getenv("PORT", default=5000))
