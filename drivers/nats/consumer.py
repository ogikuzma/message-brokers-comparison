import asyncio
import pickle
import os
from datetime import datetime, timedelta
from typing import Dict, Tuple

from drivers.nats.driver import NatsDriver
from drivers.consumer_driver_interface import ConsumerDriver


class NatsConsumer(NatsDriver, ConsumerDriver):

    async def consume_messages(self, num_of_msgs: int) -> Tuple[Dict[str, datetime], datetime]:
        
        consume_metrics = {}
        consume_metrics['message_metrics'] = {}

        messages_handled = 0
        consume_start_time = None
        total_consume_time = None

        stop_condition = asyncio.Event()

        async def message_handler(msg):
            nonlocal messages_handled, consume_start_time, total_consume_time, stop_condition

            messages_handled += 1

            # Pokreni tajmer
            if messages_handled == 1:
                consume_start_time = datetime.now()
                print("Detektovana prva poruka, konzumiranje u toku...")

            msg_consume_timestamp = datetime.now()
            message_id = msg.headers.get("Correlation-ID")
            consume_metrics['message_metrics'][message_id] = msg_consume_timestamp

            if messages_handled % 1000 == 0:
                print(f'Obradjeno {messages_handled} poruka')

            # Zaustavi konzumaciju poruka
            if messages_handled == num_of_msgs:
                print("Sve poruke obrađene. Zaustavlja se dalje konzumiranje...")
                total_consume_time = datetime.now() - consume_start_time

                stop_condition.set()
        
        await self.nats.subscribe(self.queue_name, cb=message_handler)

        print("Konzument je spreman za konzumiranje poruka...")

        await stop_condition.wait()

        return consume_metrics, total_consume_time


    def save_metrics(self, config, consume_metrics: Dict[str, datetime], total_consume_time: timedelta):
        consume_metrics['msg_size'] = config['msg_size']
        consume_metrics['num_of_msgs'] = config['num_of_msgs']
        consume_metrics['total_consume_time'] = total_consume_time

        test_name = f"{config['msg_size']}_{config['num_of_msgs']}"

        save_path = f"results/{config['env']}/nats/{test_name}"
        
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        with open(f"{save_path}/consume_metrics.pkl", 'wb') as f:
            pickle.dump(consume_metrics, f)


    async def start(self, config):

        await self.init_connection()

        consume_metrics, total_consume_time = await self.consume_messages(config['num_of_msgs'])

        await self.close_connection()
        
        self.save_metrics(config, consume_metrics, total_consume_time)
    