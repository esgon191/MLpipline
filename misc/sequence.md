```uml
@startuml

actor "Фронт" as f
participant "CRUD (Бэкенд)" as c
f -> c: Поступившая фотография
activate c

database "SQL (PostgreSQL)" as sql
database "S3 (MinIO)" as s3
group Сохранение фотографии
c ->> sql: Помещение метаданных, открытие транзакции
activate sql
sql --> c: Возврат присвоенного id
c ->> s3: Помещение тела фотографии
c ->> sql: Коммит транзакции
deactivate sql
end
participant "Kafka" as k

c ->> k: Помещение фотографии в очередь на обработку

@enduml
```