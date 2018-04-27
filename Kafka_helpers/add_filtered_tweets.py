from kafka import KafkaProducer, KafkaConsumer
import argparse
import json
import os
import io

kafka_topic = 'mock_twitter_stream'
number = 9974

consumer = KafkaConsumer(bootstrap_servers='localhost:9092')

partitions = consumer.partitions_for_topic(kafka_topic)
topic_partitions = list()
for partition in partitions:
    topic_partitions.append(TopicPartition(kafka_topic, partition))

consumer.assign(topic_partitions)
consumer.seek_to_end()

topic_partition_to_offset = dict()
for topic_partition in topic_partitions:
    next_offset = consumer.position(topic_partition)
    reduced_offset = max(next_offset - number, 0)
    topic_partition_to_offset[topic_partition] = reduced_offset

for topic_partition, offset in topic_partition_to_offset.items():
    consumer.seek(topic_partition, offset)

count = 0
for message in consumer:
    count += 1

    try:
        value = json.loads(message.value.decode())
        print value
        input()
    except:
        value = message.value.decode()
