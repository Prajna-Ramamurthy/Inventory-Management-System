import pika
from flask import Flask
import time

time.sleep(2)

app = Flask(__name__)

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.1'))
channel = connection.channel()


# Microservice for checking the health of the RabbitMQ connection
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue='healthcheck', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='healthcheck',
        body="Health check message sent",
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
    ))
    connection.close()
    print("Health check message sent")
    return "Health check message sent\n"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
