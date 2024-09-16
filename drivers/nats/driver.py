import nats

from drivers.driver_interface import DriverInterface
from credentials.credentials import credentials_params

class NatsDriver(DriverInterface):

    queue_name = 'main_queue'

    async def init_connection(self):
        self.nats = await nats.connect(f"nats://{credentials_params['nats']['hostname']}:{credentials_params['nats']['port']}") 


    def setup_testing_infrastructure(self):
        pass
    

    async def close_connection(self):
        await self.nats.drain()
        await self.nats.close()