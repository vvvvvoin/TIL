import requests
from decouple import config


#token ="933788991:AAG6SIc5WbH6vWe06dapNwo4a6jJFjbhh6A"
token = config('telegram_bot_token')
app_url = f"https://api.telegram.org/bot{token}"
chat_id = config('chat_id')

#update_url = app_url + "/getUpdates"
#response = requests.get(update_url).json()
#print(response)
#                  dict     list    dict
#chat_id = response["result"][0]["message"]["chat"]["id"]
#print(chat_id)

text = "check"
message_url = app_url + f"/sendMessage?chat_id={chat_id}&text={text}"

requests.get(message_url)