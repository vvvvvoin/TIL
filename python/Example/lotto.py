import random
import requests
from bs4 import BeautifulSoup as bs
import json

number = random.sample(range(1, 46), 6)
url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=836"
print(sorted(number))

response = requests.get(url)
print(response.text)

lotto = json.loads(response.text) # 글자를 dirct 클래스로 변환
print(lotto)

# print(lotto["drwtNo5"]) ## 데이터 값이 없으면 오류발생
# print(lotto.get(["drwtNo5"])) ## 데이터 값이 없으면 none 반환

winner = []
for i in range(1, 7):
    winner.append(lotto.get(f"drwtNo{i}"))

print(winner)





