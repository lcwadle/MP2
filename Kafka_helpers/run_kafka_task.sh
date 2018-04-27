#!/bin/bash

# Create mock_twitter_stream topic
#../../bin/kafka-topics.sh \
#  --create \
#  --zookeeper localhost:2181 \
#  --replication-factor 1 \
#  --partitions 1 \
#  --topic mock_twitter_stream

# Create mock_twitter_stream topic
#../../bin/kafka-topics.sh \
#  --create \
#  --zookeeper localhost:2181 \
#  --replication-factor 1 \
#  --partitions 1 \
#  --topic spark_input

# Read input file and save in mock_twitter_stream
python add_tweets.py

# Read input file and save in mock_twitter_stream
#python add_filtered_tweets.py
