#!/usr/bin/env python
import time

import pika, sys, os
import json


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='push_app_123', durable=True)

    def callback(ch, method, properties, body):
        msg = json.loads(body.decode())
        print(f" [x] Received {msg}")
        time.sleep(0.5)
        print(f"Delivery tag {method.delivery_tag}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='push_app_123', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
