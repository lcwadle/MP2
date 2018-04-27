import base64
import hashlib
import hmac
import json
import oauth2
import random
import requests
import time

SETTINGS_FILE_NAME = 'settings.json'
OUTPUT_FILE_NAME = 'tweets.txt'
TOPICS = ['database', 'SQL', 'MapReduce', 'data', 'RDBMS', 'DBMS', 'NoSQL',
          'Spark', 'Kafka', 'MongoDB', 'SIGMOD']
LANGUAGES = ['en']
TARGET_COUNT = 10000


def load_settings():
    with open(SETTINGS_FILE_NAME, 'rt') as settings_file:
        settings = json.load(settings_file)

    return settings


def create_nonce():
    bs = bytearray(random.getrandbits(8) for _ in range(32))
    return base64.urlsafe_b64encode(bs).decode()


def add_signature(settings, url, data):
    method = 'POST'
    encoded = [(oauth2.escape(k), oauth2.escape(v)) for k, v in data.items()]
    encoded = sorted(encoded, key=lambda t: t[0])
    items = ['{}={}'.format(k, v) for k, v in encoded]
    param_string = '&'.join(items)
    signature_base = '&'.join([method, oauth2.escape(url),
                               oauth2.escape(param_string)])
    c_secret = settings['consumer_secret']
    o_secret = settings['access_token_secret']
    key = '&'.join([oauth2.escape(c_secret), oauth2.escape(o_secret)])
    hashed = hmac.new(bytes(key, 'utf-8'), bytes(signature_base, 'utf-8'),
                      hashlib.sha1)
    signature = base64.b64encode(hashed.digest()).decode()
    data['oauth_signature'] = signature


def download_tweets(settings):
    url = settings['stream_api_url']
    data = {
        'oauth_consumer_key': settings['consumer_key'],
        'oauth_nonce': create_nonce(),
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_token': settings['access_token'],
        'oauth_version': '1.0',
        'track': ','.join(TOPICS),
        'language': ','.join(LANGUAGES),
    }
    add_signature(settings, url, data)
    auth_header = 'OAuth {}'.format(
        ','.join(['{}="{}"'.format(k, v) for k, v in data.items()]))
    headers = {'Authorization': auth_header}
    r = requests.post(url, data=data, headers=headers, stream=True)
    tweets = list()
    count = 0
    for line in r.iter_lines():
        try:
            tweets.append(json.loads(line))
            print(tweets[-1]['text'])
        except Exception as e:
            print(e)

        print(count)
        count += 1
        if count == TARGET_COUNT:
            return tweets

    return tweets


def write_to_file(tweets):
    with open(OUTPUT_FILE_NAME, 'wt') as output_file:
        for tweet in tweets:
            output_file.write('{}\n'.format(json.dumps(tweet)))


def main():
    settings = load_settings()
    tweets = download_tweets(settings)
    write_to_file(tweets)


if __name__ == '__main__':
    main()
