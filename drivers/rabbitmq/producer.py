import pickle
import pika
from datetime import datetime, timedelta
from typing import Dict, Tuple

from drivers.producer_driver_interface import ProducerDriver
from drivers.rabbitmq.driver import RabbitMqDriver


class RabbitMqProducer(RabbitMqDriver, ProducerDriver):


    def publish_messages(self, msg_path: str, num_of_msgs: int) -> Tuple[Dict[int, datetime], datetime]:
        channel = self.connection.channel()

        message = None
        produce_metrics = {}

        # Pripremi sadržaj poruke
        with open(msg_path, 'r') as file:
            message = file.read()

        print("Kreće generisanje poruka...")

        produce_metrics = {}
        produce_metrics['message_metrics'] = {}

        # Pokreni tajmer
        produce_start_time = datetime.now()

        # Objavi poruke
        for i in range(num_of_msgs):
            message_id = str(i)
            produce_metrics['message_metrics'][message_id] = datetime.now()
            channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(correlation_id=message_id)
            )

            if i % 1000 == 0 and i > 0:
                print(f'Generisano {i} poruka')

        total_publish_time = datetime.now() - produce_start_time

        print("Završeno generisanje poruka")
        
        return produce_metrics, total_publish_time


    def save_metrics(self, config, produce_metrics: Dict[str, datetime], total_publish_time: timedelta):
        produce_metrics['msg_size'] = config['msg_size']
        produce_metrics['num_of_msgs'] = config['num_of_msgs']
        produce_metrics['total_publish_time'] = total_publish_time

        with open('results/rabbitmq/produce_metrics.pkl', 'wb') as f:
            pickle.dump(produce_metrics, f)


    def start(self, config):

        self.init_connection()

        produce_metrics, total_publish_time = self.publish_messages(config['msg_path'], config['num_of_msgs'])

        self.close_connection()

        self.save_metrics(config, produce_metrics, total_publish_time)