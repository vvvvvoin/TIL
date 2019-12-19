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
print(doc.select_one("#PM_ID_ct > div.header > div.section_navbar > div.area_hotkeyword.PM_CL_realtimeKeyword_base > div.ah_list.PM_CL_realtimeKeyword_list_base > ul:nth-child(5) > li.ah_item.ah_on > a > span.ah_k").text)

# search_url = "https://search.naver.com/search.naver?query="
# for i in range(5) :
#     webbrowser.open(search_url + result[i].text)







