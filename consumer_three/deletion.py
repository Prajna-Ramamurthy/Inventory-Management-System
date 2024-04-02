import pika, json
import time
import logging

time.sleep(10)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='stock_management', durable=True)

# Callback function for stock management
def callback(ch, method, properties, body):
    logging.info('Stock Management callback function is called!')
    data = json.loads(body)

    if not connection.is_closed:
        print("Stock Management message received: ", data)
        logging.info('Stock Management message received: %s', data)
    else:
        print("Stock Management unsuccessful! Connection not found!")
        logging.error('Stock Management unsuccessful! Connection not found!')

    return "Stock Management is done!"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='stock_management', 
                      on_message_callback=callback, 
                      auto_ack=True)

print ('Starting consuming')
logging.info('Starting consuming')

channel.start_consuming()

channel.close() # close channel on exit