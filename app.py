import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from imgurpython import ImgurClient
from flask import Flask,request,abort
from linebot import (LineBotApi,WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
app = Flask(__name__) #宣告一個變數掌控你的server
line_bot_api=LineBotApi("0TCWng6lRIsTXuAG0nzi4k+MWHiU/iDm4DMSF48Dm1gun2B8UvRzkrbGeqtA5G94Te8VilwPDqukiCNqHi6jGB2UvEillhm999JAo8H9JqU9nzDGtXKTQQFsXFRL+0B+69UP7r8S/a9wx3n9W/PJpQdB04t89/1O/w1cDnyilFU=")

handler=WebhookHandler("b1e57b22301fed40155006da2589530e")

#監聽所有東西/callback的post request
@app.route("/callback", methods=['POST'])#route叫做裝飾器,會幫你對應到url
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body:"+body)
    try:
        handler.handle(body,signature)#會判斷要用哪個設定來回應event
    except InvalidSignatureError:#檢查你的資料是否正確
        abort(400)
    return "ok"
def apple_news():
    target_url = "https://tw.appledaily.com/new//realtime"
    print("Start parsing applenews....")
    rs = requests.session()
    res =rs.get(target_url,verify =False)
    soup =BeautifulSoup(res.text,"html.parser")
    content = ""
    for index,data in enumerate(soup.select(".rtddt a"),0):
        if index==5:
            return content
        link = data["href"],
        content+="{}\n\n".format(link)
    return content
def technews():
    target_url = "https://technews.tw/"
    print("Start parsing movie ..")
    rs = requests.session()
    res = rs.get(target_url,verify=False)
    res.encoding ="utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    content=""
    
    for index,data in enumerate(soup.select("article div h1.entry-title a")):
        if index==12:
            return content
        title = data.text
        link = data["href"]
        content+="{}\n{}\n\n".format(title,link)
    return content
def movies_1():
    target_url = "https://movies.yahoo.com.tw/movie_thisweek.html"
    print("Start parsing...")
    rs = requests.session()
    res = rs.get(target_url,verify=False)
    res.encoding ="utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    content=""

    for index,data in enumerate(soup.select("li div.release_movie_name a")):
        if index==10:
            return content
        title = data.text
        link = data["href"]
        content+="{}\n{}\n\n".format(title,link)
    return content
def movies_2():
    target_url = "https://movies.yahoo.com.tw/movie_intheaters.html"
    print("Start parsing...")
    rs = requests.session()
    res = rs.get(target_url,verify=False)
    res.encoding ="utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    content=""

    for index,data in enumerate(soup.select("li div.release_movie_name a")):
        if index==10:
            return content
        title = data.text
        link = data["href"]
        content+="{}\n{}\n\n".format(title,link)
#處理訊息
@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    #應聲鳥回應文字訊息
    #message = TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token,message)

    #line官方貼圖的回應
    #message = StickerSendMessage(package_id="11537",sticker_id="52002767")
    #line_bot_api.reply_message(event.reply_token,message)
    print("event.reply_token:",event.reply_token)
    print("event.message.text:",event.message.text)
    if event.message.text=="開始玩":
        buttons_template = TemplateSendMessage(
            alt_text = "開始玩template",
            template = ButtonsTemplate(
                title = "選擇服務",
                text="請選擇",
                thumbnail_image_url="https://i.imgur.com/xQF5dZT.jpg",
                actions=[
                    MessageTemplateAction(
                        label = "新聞",
                        text = "新聞",
                    ),
                    MessageTemplateAction(
                        label="看電影",
                        text="看電影"
                    ),
                    MessageTemplateAction(
                        label="看廢文",
                        text="看廢文",    
                    ),
                    MessageTemplateAction(
                        label="正妹",
                        text="正妹"
                    )]))
        line_bot_api.reply_message(event.reply_token,buttons_template)
        return 0      
    if event.message.text=="新聞":
        buttons_template = TemplateSendMessage(
            alt_text = "新聞 template",
            template = ButtonsTemplate(
                title = "新聞類型",
                text="請選擇",
                thumbnail_image_url="https://i.imgur.com/7LrroAW.jpg",
                actions=[
                    MessageTemplateAction(
                        label = "蘋果即時新聞",
                        text = "蘋果即時新聞",
                    ),
                    MessageTemplateAction(
                        label="科技新報",
                        text="科技新報"
                    ),
                    MessageTemplateAction(
                        label="PanX泛科技",
                        text="PanX泛科技",    
                    ),
                    MessageTemplateAction(
                        label="正妹",
                        text="正妹"
                    )]))
        line_bot_api.reply_message(event.reply_token,buttons_template)
        return 0
    if event.message.text == "蘋果即時新聞":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "科技新報":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text=="看電影":
        buttons_template = TemplateSendMessage(
            alt_text = "電影 template",
            template = ButtonsTemplate(
                title="movie",
                text="請選擇",
                thumbnail_image_url="https://i.imgur.com/9Jnve0x.jpg",
                actions=[
                    MessageTemplateAction(
                        label = "本週新片",
                        text = "本週新片",
                    ),
                    MessageTemplateAction(
                        label="上映中",
                        text="上映中"
                    ),
                    MessageTemplateAction(
                        label="即將上映",
                        text="即將上映",    
                    )]))
        line_bot_api.reply_message(event.reply_token,buttons_template)
        return 0
    if event.message.text == "本週新片":
        content = movies_1()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "上映中":
        content = movies_2()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "即將上映":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0 
    message = TemplateSendMessage(
    alt_text="目錄template",
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/Yn5QXpf.jpg",
                title = "選擇服務",
                text = "請選擇",
                actions=[
                    MessageAction(
                        label = "開始玩",
                        text = '開始玩'),
                    URIAction(
                        label="stranger things",
                        uri = "https://www.youtube.com/watch?v=9ynAk_VeBLc"),
                    URIAction(
                        label="money heist",
                        uri = "https://www.youtube.com/watch?v=TFJwUwnShnA")]),
            CarouselColumn(
                thumbnail_image_url="https://i.imgur.com/9Jnve0x.jpg",
                title="選擇服務",
                text="請選擇",
                actions=[
                    MessageAction(
                        label="程式學習",
                        text="程式學習！"),
                    URIAction(
                        label="codecademy",
                        uri="https://www.codecademy.com/login"),
                    URIAction(
                        label="code camp",
                        uri="https://www.freecodecamp.org")])]))
    line_bot_api.reply_message(event.reply_token,message)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0,len(sticker_ids)-1)
    sticker_id =str(sticker_ids[index_id])
    print(sticker_id)
    sticker_message = StickerSendMessage(
        package_id= "1",
        sticker_id = sticker_id
    )
    line_bot_api.reply_message(event.reply_token,sticker_message)
import os
if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
