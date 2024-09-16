from datetime import datetime, timedelta
from typing import Dict

from drivers.producer_driver_interface import ProducerDriver
from rocketmq.client import Producer, Message


class RocketMqProducer(ProducerDriver):

    def publish_messages(self, connection, msg_path: str, num_of_msgs: int):

        producer = Producer('testGroup')
        producer.set_name_server_address('localhost:9876')

        producer.start()

        try:
            for i in range(10):
                # Create a new message with a topic
                msg = Message('testTopic')
                # Set message body
                msg.set_body(f"Hello RocketMQ {i}")
                # Send the message
                ret = producer.send_sync(msg)
                print(f"Message sent: {ret.status}, message ID: {ret.msg_id}")

        except Exception as e:
            print(f"Exception: {e}")



    def save_metrics(args, produce_metrics: Dict[str, datetime], total_publish_time: timedelta):
        pass

    def start(self, config):
        self.publish_messages()