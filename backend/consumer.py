import json
import requests
import pika
# from .app import addreview

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='blog')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    if properties.content_type == 'add':
        body = json.loads(body)
        # res = addreview(body)
        res = requests.post("http://backend:5000/reviews/add", data=body)
        print(res)

channel.basic_consume(on_message_callback=callback, queue='blog', auto_ack=True)
print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()