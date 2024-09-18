import pika

from credentials.credentials import credentials_params
from drivers.driver_interface import DriverInterface


class RocketMqDriver(DriverInterface):

    queue_name = 'main_queue'
    group_name = 'testGroup'

    def init_connection(self):
        self.connection_url = f"{credentials_params['rocketmq']['hostname']}:{credentials_params['rocketmq']['port']}"
        

    def setup_testing_infrastructure(self):
        pass
    

    def close_connection(self):
        pass