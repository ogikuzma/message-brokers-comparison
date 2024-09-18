from datetime import datetime, timedelta
import pickle
from typing import Dict

from drivers.producer_driver_interface import ProducerDriver
from drivers.rocketmq.driver import RocketMqDriver
from rocketmq.client import Producer, Message


class RocketMqProducer(RocketMqDriver, ProducerDriver):

    def publish_messages(self, msg_path: str, num_of_msgs: int):

        producer = Producer(self.group_name)
        producer.set_name_server_address(self.connection_url)
        producer.set_max_message_size(5242880) # 5MB

        message = None

        # Pripremi sadržaj poruke
        with open(msg_path, 'r') as file:
            message = file.read()

        produce_metrics = {}
        produce_metrics['message_metrics'] = {}

        producer.start()
        print("Kreće generisanje poruka...")
        
        # Pokreni tajmer
        produce_start_time = datetime.now()

        for i in range(num_of_msgs):
            message_id = str(i)
            produce_metrics['message_metrics'][message_id] = datetime.now()

            msg = Message(self.queue_name)
            msg.set_property('correlationId', message_id)
            msg.set_body(message)

            producer.send_sync(msg)
        
            if i % 1000 == 0 and i > 0:
                print(f'Generisano {i} poruka')

        total_publish_time = datetime.now() - produce_start_time

        print("Završeno generisanje poruka")
        producer.shutdown()
        
        return produce_metrics, total_publish_time


    def save_metrics(self, config, produce_metrics: Dict[str, datetime], total_publish_time: timedelta):
        produce_metrics['msg_size'] = config['msg_size']
        produce_metrics['num_of_msgs'] = config['num_of_msgs']
        produce_metrics['total_publish_time'] = total_publish_time

        with open(f'{self.result_path}/rocketmq/produce_metrics.pkl', 'wb') as f:
            pickle.dump(produce_metrics, f)
            

    def start(self, config):

        self.init_connection()
        
        produce_metrics, total_publish_time = self.publish_messages(config['msg_path'], config['num_of_msgs'])

        self.save_metrics(config, produce_metrics, total_publish_time)