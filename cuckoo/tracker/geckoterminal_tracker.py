from typing import List

from cuckoo.base import Messenger, Observer
from cuckoo.datasource.geckoterminal import Geckoterminal
from cuckoo.tracker.token_tracker import TokenTracker
from cuckoo.utils import (
    TOKEN_POOL_ADDRESS,
    TOKEN_POOL_ATTRIBUTE,
    TOKEN_POOL_NAME,
    TOKEN_POOL_NETWORK,
)


class GeckoterminalTracker(TokenTracker):
    def __init__(
        self, pools: List[dict], displays: List[Observer], messengers: List[Messenger]
    ) -> None:
        handlers: List[Observer] = []
        handlers.extend(displays)
        pool_infos: List[Geckoterminal.PoolInfo] = []
        for pool in pools:
            pool_infos.append(
                Geckoterminal.PoolInfo(
                    pool[TOKEN_POOL_NETWORK],
                    pool[TOKEN_POOL_ADDRESS],
                    pool[TOKEN_POOL_ATTRIBUTE],
                )
            )
            processors = self.get_processors(pool)
            handlers.extend(
                self.get_price_checker(pool[TOKEN_POOL_NAME], processors, messengers)
            )

        super().__init__(Geckoterminal(pool_infos), handlers)
