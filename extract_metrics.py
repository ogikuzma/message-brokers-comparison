import pickle
from datetime import datetime
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

from config_parser.config_parser import get_parsed_config


def calculate_result(config, consume_metrics: Dict[str, datetime], produce_metrics: Dict[str, datetime]):
    msg_broker = config['msg_broker']
    msg_size = consume_metrics['msg_size']
    num_of_msgs = int(consume_metrics['num_of_msgs'])

    total_consume_time = consume_metrics['total_consume_time']
    total_publish_time = produce_metrics['total_publish_time']

    all_times = []
    for message_id in consume_metrics['message_metrics']:
        time_diff = consume_metrics['message_metrics'][message_id] - produce_metrics['message_metrics'][message_id]
        all_times.append(time_diff.total_seconds())
    
    np_array = np.array(all_times)
    mean_time = np.mean(np_array)
    median = np.percentile(np_array, 50)
    p95 = np.percentile(np_array, 95)
    p99 = np.percentile(np_array, 99)

    print(
        f"""\n
        Broker: RabbitMQ
        Broj poruka: {num_of_msgs}
        Veličina poruke: {msg_size.title()}
        Kašnjenje - Prosečno vreme obrade jedne poruke: {round(mean_time, 2)}s
        Kašnjenje - Medijana: {round(median, 2)}s
        Kašnjenje - p95: {round(p95, 2)}s
        Kašnjene - p99: {round(p99, 2)}s
        Ukupno vreme za objavljivanje poruka: {round(total_publish_time.total_seconds(), 2)}s
        Ukupno vreme za konzumiranje poruka: {round(total_consume_time.total_seconds(), 2)}s\n
        Protok - {round(num_of_msgs / total_publish_time.total_seconds(), 2)} objavljenih poruka u jedinici vremena
        Protok - {round(num_of_msgs / total_consume_time.total_seconds(), 2)} konzumiranih poruka u jedinici vremena
        """
    )

    plt.figure().set_figwidth(10)
    plt.hist(np_array)

    plt.title(f"Histogram kašnjenja obrade poruka: {msg_broker.title()} - {num_of_msgs:,} poruka - {msg_size.title()} veličina poruke", loc = 'left')
    plt.xlabel("Kašnjenje (s)")
    plt.ylabel("Broj poruka")
    
    plt.show()


if __name__ == "__main__":
    
    # Pročitaj parametre testa
    config = get_parsed_config()

    with open(f'results/{config["msg_broker"]}/produce_metrics.pkl', 'rb') as file:
        produce_metrics = pickle.load(file)

    with open(f'results/{config["msg_broker"]}/consume_metrics.pkl', 'rb') as file:
        consume_metrics = pickle.load(file)

    calculate_result(config, consume_metrics, produce_metrics)