curl -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '
	{
	"name": "postgres-connector", 
	"config": { 
	"connector.class": "io.debezium.connector.postgresql.PostgresConnector", 
	"tasks.max": "1",
	"database.hostname": "postgres_booking",
	"database.port": "5432",
	"database.user": "postgres",
	"database.password": "postgres",
	"database.dbname" : "postgres",
	"database.server.name": "booking",
	"database.history.kafka.bootstrap.servers": "kafka-1:9092,kafka-2:9092",
	"plugin.name": "pgoutput"
	}
	}'