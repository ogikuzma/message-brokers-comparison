import asyncio
import json

from config_parser.config_parser import get_parsed_config
from drivers.nats.consumer import NatsConsumer
from drivers.rabbitmq.consumer import RabbitMqConsumer


if __name__ == '__main__':
    
    # Pročitaj parametre testa
    config = get_parsed_config()

    # Pokreni konzumenta poruka
    if config['msg_broker'] == 'rabbitmq':
        RabbitMqConsumer().start(config)
    elif config['msg_broker'] == 'nats':
        consumer = NatsConsumer()
        asyncio.run(consumer.start(config))

