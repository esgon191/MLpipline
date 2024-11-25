docker-compose -p kursovaya up -d

docker exec kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic a_topic --partitions 3 --replication-factor 3
docker exec kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic b_topic --partitions 3 --replication-factor 3
docker exec kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic saver_topic --partitions 3 --replication-factor 3

#zsh topics.sh