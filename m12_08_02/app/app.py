#!/usr/bin/env python
from datetime import datetime

import pika
import json

from models import Task

credentials = pika.PlainCredentials('pglbwiuh', '****')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='sparrow-01.rmq.cloudamqp.com', port=5672, credentials=credentials, virtual_host='pglbwiuh'))
channel = connection.channel()

channel.exchange_declare(exchange='test_service', exchange_type='direct')
channel.queue_declare(queue='test_campaign', durable=True)
channel.queue_bind(exchange='test_service', queue='test_campaign')


def main():
    for i in range(100):
        task = Task(consumer="Noname").save()

        channel.basic_publish(exchange='test_service', routing_key='test_campaign', body=str(task.id).encode(),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    connection.close()


if __name__ == '__main__':
    main()
