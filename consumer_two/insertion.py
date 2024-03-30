from flask import Flask
import time
import pika

time.sleep(2)

app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.1'))
channel = connection.channel()
channel.queue_declare(queue='insert_record', durable=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)