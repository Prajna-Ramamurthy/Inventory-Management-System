import pika, json
import time
import logging

time.sleep(10)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='order_processing', durable=True)

# Callback function for order processing
def callback(ch, method, properties, body):
    logging.info('Order Processing callback function is called!')
    data = json.loads(body)

    if not connection.is_closed:
        print("Order Processing message received: ", data)
        logging.info('Order Processing message received: %s', data)
    else:
        print("Order Processing unsuccessful! Connection not found!")
        logging.error('Order Processing unsuccessful! Connection not found!')

    return "Order Processing is done!"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='order_processing', 
                      on_message_callback=callback, 
                      auto_ack=True)

print ('Starting consuming')
logging.info('Starting consuming')

channel.start_consuming()

channel.close() # close channel on exit
