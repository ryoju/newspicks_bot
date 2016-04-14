# -*- coding: utf-8 -*-

import os
import json
import requests

from django.http import JsonResponse
from django.views.generic import View

from newspicks.settings_line import CHANNEL_ID, CHANNEL_SECRET, MID

from nlp.functions import find_appropriate_news, get_nouns

ENDPOINT = 'https://trialbot-api.line.me/v1/events'
PROFILES_ENDPOINT = 'https://trialbot-api.line.me/v1/profiles'

EVENT_REGISTER = '138311609100106403'
EVENT_TALK = '138311609000106303'

def post_text(send_to, content):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Line-ChannelID': CHANNEL_ID,
        'X-Line-ChannelSecret': CHANNEL_SECRET,
        'X-Line-Trusted-User-With-ACL': MID
    }
    payload = {
        'toChannel': 1383378250,
        'eventType': '138311608800106203',
        'to': send_to,
        'content': content
    }
    print (json.dumps(payload))
    req = requests.post(ENDPOINT,
                    headers=headers,
                    data=json.dumps(payload))
    print('request')
    print(req.__dict__)


def get_GTSY(user_name):
    if user_name:
        text = '{0}さん、はじめまして。ぼくはうまって言います。'.format(user_name.encode('utf-8'))
    else:
        text = 'はじめまして。ぼくはうまって言います。'
    return {
        'contentType': 1,
        'toType': 1,
        'text': text,
    }

def get_usage():
    return {
        'contentType': 1,
        'toType': 1,
        'text': '登録ありがとう。知りたいことを教えてくれたら、NewsPicksのよさげな記事を見つけてきます！',
    }

def get_acceptance():
    return {
        'contentType': 1,
        'toType': 1,
        'text': 'ちょっとまっててね...',
    }

def get_found():
    return {
        'contentType': 1,
        'toType': 1,
        'text': 'こんなのはどうかな？',
    }

def get_title(news):
    if news['picker']:
        text = '『{0}』っていう記事だよ。{1}さんのコメントがとっても参考になるよ！'.format(
            news['title'].encode('utf-8'),
            news['picker'].encode('utf-8')
        )
    else:
        text = '『{0}』っていう記事だよ。'.format(news['title'].encode('utf-8'))
    return {
        'contentType': 1,
        'toType': 1,
        'text': text,
    }

def get_not_found():
    return {
        'contentType': 1,
        'toType': 1,
        'text': 'ごめんね、うまく見つからなかったよ。他に知りたいことはないかな？',
    }

def get_text_news(news):
    return {
        'contentType': 1,
        'toType': 1,
        'text': news['title'],
    }

def get_rich_news(news):
    return {
        'contentType': 12,
        'toType': 1,
        "contentMetadata": {
            "DOWNLOAD_URL": "http://bot.windy.ac/images/newspicks/{0}".format(news['news_id']),
            "SPEC_REV": "1",
            "ALT_TEXT": news['title'],
            "MARKUP_JSON": get_markup_json(news)
        }
    }

def get_markup_json(news):
    payload = {
      "canvas": {
        "width": 1040,
        "height": 483,
        "initialScene": "scene1"
      },
      "images": {
        "image1": {
          "x": 0,
          "y": 0,
          "w": 1040,
          "h": 483
        }
      },
      "actions": {
        "link1": {
          "type": "web",
          "text": news['title'],
          "params": {
            "linkUri": news['url']
          }
        },
        "link2": {
          "type": "web",
          "text": news['title'],
          "params": {
            "linkUri": news['url']
          }
        }
      },
      "scenes": {
        "scene1": {
          "draws": [
            {
              "image": "image1",
              "x": 0,
              "y": 0,
              "w": 1040,
              "h": 483
            }
          ],
          "listeners": [
            {
              "type": "touch",
              "params": [0, 0, 1040, 100],
              "action": "link1"
            },
            {
              "type": "touch",
              "params": [0, 100, 1040, 483],
              "action": "link2"
            }
          ]
        }
      }
    }
    return json.dumps(payload)

def get_user_name(user):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Line-ChannelID': CHANNEL_ID,
        'X-Line-ChannelSecret': CHANNEL_SECRET,
        'X-Line-Trusted-User-With-ACL': MID
    }
    payload = {
        'mids': user,
    }
    print (json.dumps(payload))
    req = requests.get(PROFILES_ENDPOINT,
                    headers=headers,
                    params=payload)
    print('request')
#    print(req.__dict__)
    print(req.json())
    try:
        return req.json()['contacts'][0]['displayName']
    except:
        return None

def response_to_talk(send_to, message):
    post_text(send_to, get_acceptance())
    news = find_appropriate_news(message)
    if news:
        post_text(send_to, get_found())
        post_text(send_to, get_title(news))
        #post_text(send_to, get_text_news(message))
        post_text(send_to, get_rich_news(news))
    else:
        post_text(send_to, get_not_found())

def response_to_register(send_to):
    user_name = get_user_name(send_to[0])
    post_text(send_to, get_GTSY(user_name))
    post_text(send_to, get_usage())

def dispose(results):
    for result in results:
        event_type = result['eventType']
        if event_type == EVENT_REGISTER:
            send_to = [result['content']['params'][0]]
            operation_type = result['content']['opType']
            if int(operation_type) == 4:
                response_to_register(send_to)
        elif event_type == EVENT_TALK:
            send_to = [result['content']['from']]
            text = result['content']['text']
            response_to_talk(send_to, text)


class NewsPicksView(View):
    http_method_names = ['get', 'post']

    def get(self, *args, **kwargs):
        return JsonResponse({'':''})

    def post(self, request, *args, **kwargs):
        print request.body
        dispose(json.loads(request.body.decode("utf-8"))['result'])
        return JsonResponse({'status': 'ok'})
