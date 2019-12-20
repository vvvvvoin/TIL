from flask import Flask, render_template, request
from decouple import config
import requests
import random

app = Flask(__name__)

token = config('telegram_bot_token')
char_id = config('chat_id')

app_url = f"https://api.telegram.org/bot{token}"
message_url = app_url + f"/sendMessage?chat_id={char_id}&text="


#root
@app.route('/')
def hello():
    return "hello"

@app.route('/write')
def write():
    #HTML FILE
    return render_template("write.html")


@app.route('/send')
def send():
    message = request.args.get("message")
    message_url = app_url + f"/sendMessage?chat_id={char_id}&text={message}"
     # message를 받아서 telegram 메시지를 보내는 요청
    requests.get(message_url)
    return "메세지 전송 완료함"

@app.route(f"/{token}", methods=['POST'])
def telegram():
     # 실습 1 : 사용자의 아이디랑 텍스트
    #print(request.get_json())
    response = request.get_json()
    chat_id = response["message"]["chat"]["id"]
    text = response["message"]["text"]
    
    result = []
    if text == '/로또' :
        for _ in range(5):
            result.append(sorted(random.sample(range(1, 47), 6)))
        text = result

    elif text == "/점심":
        menu = ["20층", "양자강", "맥도날드", "바스버거"]
        text = random.choice(menu)

    # 앵무새
    # 실습 2 : 텔레그램 메시지 보내기 요청
    message_url = app_url + f"/sendMessage?chat_id={chat_id}&text={text}"
    requests.get(message_url)
    
        
    
    
    return '', 200












if __name__ == "__main__" :
    app.run(debug=True)
























