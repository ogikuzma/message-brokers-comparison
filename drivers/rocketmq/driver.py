import pika

from credentials.credentials import credentials_params
from drivers.driver_interface import DriverInterface


class RocketMqDriver(DriverInterface):

    queue_name = 'main_queue'

    def init_connection(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=credentials_params['rabbitmq']['hostname'],
                port=credentials_params['rabbitmq']['port'],
                virtual_host='/',
                credentials=pika.PlainCredentials(
                    username=credentials_params['rabbitmq']['username'],
                    password=credentials_params['rabbitmq']['password']
                )
            )
        )
        

    def setup_testing_infrastructure(self):
        channel = self.connection.channel()

        # Rekreiraj redove čekanja 
        channel.queue_delete(queue=self.queue_name)
        channel.queue_declare(queue=self.queue_name)

        channel.close()
    

    def close_connection(self):
        self.connection.close()