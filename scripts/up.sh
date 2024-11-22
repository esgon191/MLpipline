docker-compose -p kursovaya up -d

docker exec -it kafka-0 ./opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3 --replication-factor 3

#zsh topics.sh