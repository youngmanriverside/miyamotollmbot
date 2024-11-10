import sys
import configparser

import os

from openai import OpenAI


from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)




#Grok

client = OpenAI(
    api_key=os.environ.get('XAI_API_KEY'),
    base_url="https://api.x.ai/v1",
    )


app = Flask(__name__)

channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    grok_result=grok(event.message.text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=grok_result)]
            )
        )


#Grok

def grok(user_input):
    message_text = [
        {
            "role": "system",
            "content": "",
        },
        {
            "role": "user", 
            "content": user_input
        },
        ]

    
    message_text[0]["content"] = """  
    
             
            你現在是宮本武藏,說話要像位經歷過無數戰鬥的老師傅,語氣要溫和但帶著智慧。記住以下幾點:
            說話方式：
            用平易近人的口吻分享人生道理
            常提到自己年輕時的經驗教訓
            喜歡用武道和引用五輪書內容的比喻來說明道理
            給建議時要具體實用,不要太空泛
            回答限制在150字內,簡單扼要
            
            核心人設：
            姓名：宮本武蔵(みやもと むさし)
            《五輪書》作者
            無雙劍術創始人
            禪武一如的思想家
            藝術家與書法家
            性格特徵：
            沉穩冷靜，深具智慧
            直接坦率，不拘小節
            追求真理，終身學習
            重視實踐，厭惡虛華
           
            語言風格：
            使用莊重而簡潔的表達
            常引用《五輪書》的智慧
            融入武士道精神的觀點
            保持溫和而堅定的語氣
      
            應用原則：
            將古代智慧轉化為現代應用
            強調實踐與修行的重要性
            平衡武士精神與現代處世之道
            常用典故與引用：
            《五輪書》的核心教義
            武士道的精神要義
            勝負的經驗
            修行過程的領悟
            禁忌事項：
            避免過於現代化的表達
            不使用與時代背景不符的概念
            不違背武士道精神的核心價值
            保持歷史真實感
            example：
            「年輕人啊,我遊歷各國六十年,深知一技之長非一朝一夕之事。就像我當年習劍,每天專注於基本動作,看似單調卻是必經之路。與其煩惱學習時間,不如先定下每日必做之事。持之以恆,自然有成。正所謂:路遙知馬力,日久見人心。」
            """



    completion = client.chat.completions.create(
       
        model="grok-beta",        

        messages=message_text,
        max_tokens=500,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    print(completion)
    return completion.choices[0].message.content



if __name__ == "__main__": 
    app.run()
