'''
1. requests > naver.com
2. respons > bs4
3. webbrowser
'''

import requests
from bs4 import BeautifulSoup as bs
import webbrowser

url = "https://naver.com"
response = requests.get(url).text

# 'html.parser' > 받아오는 형식
doc = bs(response, 'html.parser')

# . > class를 가져오겠다
# # > id 값을 가져오겠다.
# result = doc.select_one('.ah_k')
# print(result)

result = doc.select('.ah_k')
print(result)

search_url = "https://search.naver.com/search.naver?query="
for i in range(5) :
     webbrowser.open(search_url + result[i].text)







