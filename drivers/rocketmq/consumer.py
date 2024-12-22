from datetime import datetime, timedelta
import os
import pickle
from typing import Dict, Tuple

from drivers.consumer_driver_interface import ConsumerDriver
from drivers.rocketmq.driver import RocketMqDriver

from rocketmq.client import PushConsumer, ConsumeStatus


class RocketMqConsumer(RocketMqDriver, ConsumerDriver):

    def consume_messages(self, num_of_msgs: int) -> Tuple[Dict[str, datetime], datetime]:

        consumer = PushConsumer(self.group_name)
        consumer.set_name_server_address(self.connection_url)

        messages_handled = 0
        consume_start_time = None
        total_consume_time = None
        stop_condition_met = False

        consume_metrics = {}
        consume_metrics['message_metrics'] = {}

        def callback(msg):
            msg_consume_timestamp = datetime.now()
            message_id = msg.get_property('correlationId').decode('utf-8')
            consume_metrics['message_metrics'][message_id] = msg_consume_timestamp

            nonlocal messages_handled, stop_condition_met, consume_start_time, total_consume_time

            messages_handled += 1

            # Pokreni tajmer
            if messages_handled == 1:
                consume_start_time = datetime.now()
                print("Detektovana prva poruka, konzumiranje u toku...")

            if messages_handled % 1000 == 0:
                print(f'Obrađeno {messages_handled} poruka')

            # Zaustavi konzumaciju poruka
            if messages_handled == num_of_msgs:
                print("Sve poruke obrađene. Zaustavlja se dalje konzumiranje...")
                total_consume_time = datetime.now() - consume_start_time
                stop_condition_met = True

            return ConsumeStatus.CONSUME_SUCCESS

        consumer.subscribe(self.queue_name, callback)
        consumer.start()
        print("Konzument je spreman za konzumiranje poruka...")

        while not stop_condition_met:
            pass

        consumer.shutdown()

        return consume_metrics, total_consume_time
        

    def save_metrics(self, config, consume_metrics: Dict[str, datetime], total_consume_time: timedelta):
        consume_metrics['msg_size'] = config['msg_size']
        consume_metrics['num_of_msgs'] = config['num_of_msgs']
        consume_metrics['total_consume_time'] = total_consume_time

        test_name = f"{config['msg_size']}_{config['num_of_msgs']}"

        save_path = f"results/{config['env']}/rocketmq/{test_name}"
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        with open(f"{save_path}/consume_metrics.pkl", 'wb') as f:
            pickle.dump(consume_metrics, f)
    

    def start(self, config):
        self.init_connection()
        
        consume_metrics, total_consume_time = self.consume_messages(config['num_of_msgs'])

        self.save_metrics(config, consume_metrics, total_consume_time)