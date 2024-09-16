from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Protocol, Tuple


class ProducerDriver(Protocol):

    @abstractmethod
    def publish_messages(self, connection, msg_path: str, num_of_msgs: int) -> Tuple[Dict[int, datetime], datetime]: raise NotImplementedError
    
    @abstractmethod
    def save_metrics(args, produce_metrics: Dict[str, datetime], total_publish_time: timedelta): raise NotImplementedError

    @abstractmethod
    def start(self, config): raise NotImplementedError