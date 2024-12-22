import asyncio
import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, Tuple

from drivers.nats.driver import NatsDriver
from drivers.producer_driver_interface import ProducerDriver


class NatsProducer(NatsDriver, ProducerDriver):

    async def publish_messages(self, msg_path: str, num_of_msgs: int) -> Tuple[datetime, datetime, Dict[int, datetime]]:

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
            
            await self.nats.publish(
                subject = self.queue_name, 
                payload = bytes(message, 'utf-8'),
                headers = {
                    "Correlation-ID": message_id
                }
            )

            if i % 1000 == 0 and i > 0:
                print(f'Generisano {i} poruka')

        total_publish_time = datetime.now() - produce_start_time

        print("Završeno generisanje poruka")

        await self.nats.flush(30)
        
        return produce_metrics, total_publish_time


    def save_metrics(self, config, produce_metrics: Dict[str, datetime], total_publish_time: timedelta):
        produce_metrics['msg_size'] = config['msg_size']
        produce_metrics['num_of_msgs'] = config['num_of_msgs']
        produce_metrics['total_publish_time'] = total_publish_time

        test_name = f"{config['msg_size']}_{config['num_of_msgs']}"

        save_path = f"results/{config['env']}/nats/{test_name}"

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        with open(f"{save_path}/produce_metrics.pkl", 'wb') as f:
            pickle.dump(produce_metrics, f)



    async def start(self, config):
        
        await self.init_connection()

        produce_metrics, total_publish_time = await self.publish_messages(config['msg_path'], config['num_of_msgs'])

        await self.close_connection()

        self.save_metrics(config, produce_metrics, total_publish_time)

            
if __name__ == "__main__":
    producer = NatsProducer()
    asyncio.run(producer.run())        