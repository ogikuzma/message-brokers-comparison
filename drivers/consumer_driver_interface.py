from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Protocol, Tuple


class ConsumerDriver(Protocol):

    @abstractmethod
    def consume_messages(self, num_of_msgs: int) -> Tuple[Dict[str, datetime], datetime]: raise NotImplementedError
    
    @abstractmethod
    def save_metrics(self, args, consume_metrics: Dict[str, datetime], total_consume_time: timedelta): raise NotImplementedError

    @abstractmethod
    def start(self, args): raise NotImplementedError
