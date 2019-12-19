import requests
from bs4 import BeautifulSoup as bs

url = "https://finance.naver.com/marketindex/"
response = requests.get(url).text
soup = bs(response, 'html.parser')

dollar = soup.select_one("#exchangeList > li.on > a.head.usd > div > span.value").text
print(f"현재 원/달러 환율은 {dollar} 입니다.")


##파일 저장
with open('test.txt', 'w', encoding='utf-8') as f:
    f.write(f"현재 원/달러 환율은 {dollar} 입니다.")

#exchangeList > li.on > a.head.usd > div > span.value
#exchangeList > li.on > a.head.jpy > div > span.value
#exchangeList > li.on > a.head.jpy