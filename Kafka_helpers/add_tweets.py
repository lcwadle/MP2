from kafka import KafkaProducer
import argparse
import json
import os

print "Begin reading tweets.txt to mock_twitter_stream"
fname = '../raw_data/tweets.txt'

with open(fname, 'r', encoding='utf-8') as f:
    content = f.readlines()
content = [x.strip() for x in content]

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
count = 0
for tweet in content:
    count += 1
    producer.send('mock_twitter_stream', tweet)

producer.flush();

print count
print "Finished reading to mock_twitter_stream"
