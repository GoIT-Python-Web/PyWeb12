#!/usr/bin/env python
import time

import pika, sys, os
import json


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    queue = channel.queue_declare(queue='', exclusive=True)
    q_name = queue.method.queue
    channel.queue_bind(exchange='Events APP', queue=q_name)

    def callback(ch, method, properties, body):
        msg = json.loads(body.decode())
        print(f" [x] Received {msg}")

    channel.basic_consume(queue=q_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
