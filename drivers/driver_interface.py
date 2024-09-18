from abc import abstractmethod
from typing import Protocol


class DriverInterface(Protocol):

    result_path = 'results'
    
    @abstractmethod
    def init_connection(self): raise NotImplementedError
    
    @abstractmethod
    def setup_testing_infrastructure(self): raise NotImplementedError

    @abstractmethod
    def close_connection(self, msg_size: str, msg_path: str, num_of_msgs: int): raise NotImplementedError