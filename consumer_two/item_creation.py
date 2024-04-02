import pika, json
import time
import logging

time.sleep(10)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='item_creation', durable=True)

# Callback function for item creation
def callback(ch, method, properties, body):
    logging.info('Item creation callback function is called!')
    data = json.loads(body)

    if not connection.is_closed:
        print("Item creation message received: ", data)
        logging.info('Item creation message received: %s', data)
    else:
        print("Item creation unsuccessful! Connection not found!")
        logging.error('Item creation unsuccessful! Connection not found!')

    return "Item creation is done!"

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='item_creation', 
                      on_message_callback=callback, 
                      auto_ack=True)

print ('Starting consuming')
logging.info('Starting consuming')

channel.start_consuming()

channel.close() # close channel on exit
