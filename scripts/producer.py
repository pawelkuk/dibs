from confluent_kafka import Producer, Consumer
import json
import random
import socket

print("Producer started...")

prod_conf = {
    "bootstrap.servers": "kafka-1:9092,kafka-2:9092",
    "client.id": socket.gethostname(),
}
producer = Producer(prod_conf)

cons_conf = {
    "bootstrap.servers": "kafka-1:9092,kafka-2:9092",
    "client.id": socket.gethostname(),
    "group.id": "group_id",
}

consumer = Consumer(cons_conf)
consumer.subscribe(["ORDERS_ENRICHED"])


def start_service():
    while True:
        msg = consumer.poll()
        import pdb

        pdb.set_trace()
        if msg is None:
            pass
        elif msg.error():
            pass
        else:
            key = msg.key()
            data = json.loads(msg.value())


def add_meats(key, data):
    producer.produce("topic", key=key, value=json.dumps(data))


if __name__ == "__main__":
    start_service()