#!/usr/bin/env python
from datetime import datetime

import pika
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='Push App Hold', exchange_type='direct')
channel.queue_declare(queue='push_app_123', durable=True)
channel.queue_bind(exchange='Push App Hold', queue='push_app_123')


def main():
    for i in range(50):
        msg = {
            "uuid": i,
            "payload": f"Date: {datetime.now().isoformat()}"
        }

        channel.basic_publish(exchange='Push App Hold', routing_key='push_app_123', body=json.dumps(msg).encode(),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    connection.close()


if __name__ == '__main__':
    main()
