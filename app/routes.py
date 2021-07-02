import os
import json
import datetime

import requests
from flask import request
from dotenv import load_dotenv

from app import app

import bot_engine

project_folder = os.path.expanduser('/home/maxilyin/bot')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.flaskenv'))


URL = f'https://api.telegram.org/bot{os.getenv("TOKEN")}/'


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def send_message(chat_id, text='some text'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)

    return r.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        print(r)
        try:
            message = r['message']['text']
            chat_id = r['message']['chat']['id']
            user_id = r['message']['from']['id']
            user_name = r['message']['from']['first_name']
            if message.startswith('/'):
                result = bot_engine.process_message(chat_id, user_id, user_name, message)
                send_message(chat_id, result)
        except Exception as e:
            with open('error_log.txt', 'w') as err_log:
                err_log.write(f'{datetime.datetime.now()} - {e.__class__.__name__}: {e}')

    return '<h1>Welcome to spending counter bot</h1>'
