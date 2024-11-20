docker-compose -p kursovaya up 

docker exec -it kafka1 kafka-topics --create --topic my-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
