import asyncio

from config_parser.config_parser import get_parsed_config
from drivers.nats.producer import NatsProducer
from drivers.rabbitmq.producer import RabbitMqProducer
from drivers.rocketmq.producer import RocketMqProducer

if __name__ == '__main__':
    
    # Pročitaj parametre testa
    config = get_parsed_config()

    # Pokreni konzumenta poruka
    if config['msg_broker'] == 'rabbitmq':
        RabbitMqProducer().start(config)
    elif config['msg_broker'] == 'nats':
        asyncio.run(NatsProducer().start(config))
    else:
        RocketMqProducer().start(config)

