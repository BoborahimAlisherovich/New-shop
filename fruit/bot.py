import requests

def send_message(text):
    url = f"https://api.telegram.org/bot6161514516:AAE8VxexYcD5ZTdGcJ-QSAJilkT6vNmhYGo/sendMessage"
    params = {"chat_id": '999588837', "text": text}
    response = requests.post(url, data=params)
    return response.json()