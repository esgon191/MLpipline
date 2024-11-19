docker exec -it kafka1 /bin/bash

kafka-topics.sh --create \
  --topic  a_topic\
  --bootstrap-server kafka1:9092 \
  --partitions 3 \
  --replication-factor 3

# Создание второго топика (topic2)
kafka-topics.sh --create \
  --topic b_topic \
  --bootstrap-server kafka1:9092 \
  --partitions 3 \
  --replication-factor 3

# Создание третьего топика (topic3)
kafka-topics.sh --create \
  --topic saver_topic \
  --bootstrap-server kafka1:9092 \
  --partitions 3 \
  --replication-factor 3