import time
import typing
from enum import Enum

from threading import Thread, Event
import logging

from .raft_client import RaftClient
module_logger = logging.getLogger(__name__)


class Result(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"

    def is_success(self) -> bool:
        return self == self.SUCCESS


class TrafficGenerator(Thread):

    def __init__(self, host: str):
        super(TrafficGenerator, self).__init__()
        self._event = Event()
        self.host = host
        self.redis_con = RaftClient(host=host, decode_responses=True)
        self.redis_con.ping()
        self._memory: typing.Dict[str, str] = {}
        self.logger = None

    def stop_traffic(self):
        """
        Tell the traffic generator to stop sending traffic and check data integrity
        """
        self._event.set()

    def check(self) -> Result:
        for k, v in self._memory.items():
            if self.redis_con.get(k) != v:
                return Result.FAILURE
        return Result.SUCCESS

    def _set_key_value(self, key: str, value: str):
        try:
            self.redis_con.set(key, value)
            self._memory[key] = value
        except Exception:
            self.logger.exception(f"Failed to set {key}, {value}")

    def should_stop(self) -> bool:
        return self._event.is_set()

    def run(self):
        self.logger = module_logger.getChild(self.name)
        self.logger.info(f"Starting traffic on redis '{self.host}' on thread '{self.name}'")

        i = 0
        while True:
            if self.should_stop():
                return

            key = f"key-{i}"
            value = f"value-{i}"
            self._set_key_value(key, value)
            i += 1
            time.sleep(1)
