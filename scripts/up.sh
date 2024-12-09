docker-compose -p kursovaya up 

docker exec kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic a_topic --partitions 3 --replication-factor 3
docker exec kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic b_topic --partitions 3 --replication-factor 3
docker exec kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic saver_topic --partitions 3 --replication-factor 3

# Настройка максимального размера сообщения 
docker exec kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --alter --topic a_topic --config max.message.bytes=6000000 --bootstrap-server localhost:9092
docker exec kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --alter --topic b_topic --config max.message.bytes=6000000 --bootstrap-server localhost:9092
docker exec kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --alter --topic saver_topic --config max.message.bytes=6000000 --bootstrap-server localhost:9092

#zsh topics.sh