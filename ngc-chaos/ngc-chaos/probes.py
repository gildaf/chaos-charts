import logging
from redis_clients import RaftClient
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SanityParams:
    host: str
    port: int = 6379


def sanity_probe(params: SanityParams):
    logger.info(f"Sanity probe: {params}")
    client = RaftClient(params.host, params.port, decode_responses=True)
    assert client.is_up()
    _test_set_get(client)


def _test_set_get(client: RaftClient):
    client.set("x", 3)
    assert int(client.get("x")) == 3




