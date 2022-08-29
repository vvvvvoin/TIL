from flask import Flask, render_template, request
import datetime
import random


#플라스크 서버의 이름이 app
app = Flask(__name__)

#url를 관리해주는 역할 @app.route("/")
@app.route("/")
def hello():
    return "안녕"

@app.route("/dday")
def dday():
    today = datetime.datetime.now()
    print(today)
    final = datetime.datetime(2020, 6, 9)
    result = final - today
    print(result)
    return f"{result.days}일 남았습니다."

@app.route("/christmas")
def christmas():
    today = datetime.datetime.now()
    month = today.date().month
    day = today.date().day
    print(today.date().strftime("%y년 %m월 %d일"))
    if (month == 12 and day == 25):
                return "<h1>예<h1>"
    else:
                return "<h1>아니요<h1>"

@app.route("/movies")
def movies():
    movies = ["해리포터", "겨울왕국2", "조커", "어바웃타임", "나홀로집에"]
    return render_template("movie.html", movies=movies, text="영화 목록")

@app.route("/greeting/<string:name>")
def greeting(name):
    print(name)
    return f"안녕하세요! {name}님"

@app.route("/cube/<int:num>")
def cube(num):
    result = num **3
    return str(result)

@app.route("/launch/<int:count>")
def launch(count):
    lanuch_list = ["짜장면", "짬봉", "볶음밥", "양장피", "탕수육", "유린만두"]
    max = len(lanuch_list)
    if len(lanuch_list) < count:
        print(f"최대 {max}까지 입력해주세요")
        return f"최대 {max}까지 입력해주세요"

    menus = random.sample(lanuch_list, count)
    print(random.sample(lanuch_list, count))
    # return f"{random.sample(lanuch_list, count)}"
    return render_template("movie.html", movies=menus, text="점심 메뉴")

    rand = random.sample(range(len(lanuch_list)), count)
    l_list =""
    for i in rand:
        l_list +=lanuch_list[i]
        print(lanuch_list[i])
    return l_list

@app.route("/vonvon")
def vonvon():
    return render_template("vonvon.html")

@app.route("/godmademe")
def godmademe():
    name = request.args.get("name")
    print(name)

    first_list = ["훈훈", "잘생김", "이상함", "특이함", "못생김", "어중간함"]
    second_list = ["애교", "잘난척", "쑥스러움", "귀여움"]
    third_list = ["허세", "식욕", "찌질", "돈복"]

    first_value = random.sample(first_list, 1)
    second_value = random.sample(second_list, 1)
    third_value = random.sample(third_list, 1)
    
    return render_template("godmademe.html", name=name, first_list=first_value, second_list=second_value,third_list=third_value)












if __name__ == "__main__":
    app.run(debug=True)






