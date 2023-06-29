#!/usr/bin/env python
import time
from datetime import datetime

import pika
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='Events APP', exchange_type='fanout')


def main():
    for i in range(20):
        time.sleep(1)
        msg = {
            "Event number": i,
            "detail": f"Event: {datetime.now().isoformat()}"
        }

        channel.basic_publish(exchange='Events APP', routing_key='', body=json.dumps(msg).encode())

    connection.close()


if __name__ == '__main__':
    main()
