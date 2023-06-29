#!/usr/bin/env python

import pika, sys, os

from models import Task


def main():
    credentials = pika.PlainCredentials('pglbwiuh', '****')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='sparrow-01.rmq.cloudamqp.com', port=5672, credentials=credentials, virtual_host='pglbwiuh'))
    channel = connection.channel()

    channel.queue_declare(queue='test_campaign', durable=True)

    def callback(ch, method, properties, body):
        pk = body.decode()
        task = Task.objects(id=pk, completed=False).first()
        if task:
            task.update(set__completed=True, set__consumer="krabaton")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='test_campaign', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
