import pika, json
from flask import Flask, jsonify, request
import time
import logging

time.sleep(8)

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the RabbitMQ connection without heartbeat, 
# as app is blocked on HTTP messages
connection = pika.BlockingConnection(
    pika.ConnectionParameters(heartbeat=0,
                              blocked_connection_timeout=300, 
                              host='rabbitmq'))
channel = connection.channel()


# Microservice for checking the health of the RabbitMQ connection
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    # channel = connection.channel()
    channel.queue_declare(queue='healthcheck', durable=True)
    print("Sending Health check message")
    logging.info('Sending Health check message')
    channel.basic_publish (
        exchange='',
        routing_key='healthcheck',
        body=json.dumps(["message", "Healthcheck"]),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    # connection.close()
    return jsonify({
        'message': 'Health check message sent'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    print("App getting terminated. Closing connection!")
    logging.info('App getting terminated. Closing connection!')
    connection.close()
