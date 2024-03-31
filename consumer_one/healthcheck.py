from flask import Flask
import pika
import time

time.sleep(10)

app = Flask(__name__)

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='healthcheck', durable=True)


# Simple Flask route for checking the health of the RabbitMQ connection
@app.route('/healthcheck')
def callback(ch, method, properties, body):
    if not connection.is_closed:
        print("Healthcheck is successful!")
    else:
        print("Healthcheck unsuccessful! Connection not found!")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return "Healthcheck is done!"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='healthcheck', on_message_callback=callback)
channel.start_consuming()