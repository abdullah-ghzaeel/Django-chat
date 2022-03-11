#!/usr/bin/env python
import pika

#credentials = pika.PlainCredentials('admin', 'admin')
#parameters = pika.ConnectionParameters('192.168.1.10',
#                                   5672,
#                                   '/',
#                                   credentials)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
def publish(message):
      channel.basic_publish(exchange='',
                            routing_key='task_queue',
                            body=message,
                            properties=pika.BasicProperties(delivery_mode=2) # make message persistent
                            )
