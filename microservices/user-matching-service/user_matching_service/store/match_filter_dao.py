from ploomy import BloomConfig, BloomFilter
from persona_sync_pylib.utils.singleton import singleton

from ..utils.environment import (
    BLOOMD_HOST,
    BLOOMD_PORT,
    BLOOMD_TIMEOUT,
    BLOOMD_FILTER_NAME,
    BLOOMD_CAPACITY,
    BLOOMD_PROBABILITY,
)


@singleton
class MatchFilterDAO:
    def __init__(self) -> None:
        config = BloomConfig(
            host=BLOOMD_HOST,
            port=BLOOMD_PORT,
            timeout=BLOOMD_TIMEOUT,
        )
        self.__filter = BloomFilter(config=config)
        self.__filter.create(
            filter_name=BLOOMD_FILTER_NAME,
            capacity=BLOOMD_CAPACITY,
            prob=BLOOMD_PROBABILITY,
        )

    def get_filter(self) -> BloomFilter:
        return self.__filter
