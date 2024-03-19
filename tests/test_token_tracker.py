import os

from cuckoo.datasource.coingecko import Coingecko
from cuckoo.datasource.geckoterminal import Geckoterminal
from cuckoo.handler.checker_handler import CheckerHandler
from cuckoo.handler.watcher_handler import WatcherHandler
from cuckoo.messenger.console_sender import ConsoleSender
from cuckoo.messenger.email_sender import EmailSender
from cuckoo.processor.simple_processor import SimpleProcessor
from cuckoo.tracker.token_tracker import TokenTracker

MAIL_RECEIVER = os.environ["MAIL_RECEIVER"]
email_sender = EmailSender(MAIL_RECEIVER)

watcher = WatcherHandler()

messengers = []
console_sender = ConsoleSender()
messengers.append(console_sender)
messengers.append(email_sender)


def test_coingecko():
    token1 = "bonk"
    crossing_up_price = 0.000030
    crossing_down_price = 0.000028
    token2 = "solana"

    datasource = Coingecko(token1, token2)
    tracker = TokenTracker(datasource)
    tracker.attach(watcher)

    high_processor = SimpleProcessor(
        crossing_up_price, SimpleProcessor.Condition.GREATER_OR_EQUAL
    )
    high_checker = CheckerHandler(token1, high_processor, messengers)
    tracker.attach(high_checker)

    low_processor = SimpleProcessor(
        crossing_down_price, SimpleProcessor.Condition.LESS_OR_EQUAL
    )
    low_checker = CheckerHandler(token1, low_processor, messengers)
    tracker.attach(low_checker)
    tracker.fetch()

    assert tracker.tokens[token1].price
    assert tracker.tokens[token2].price


def test_geckoterminal():
    pool_address1 = "0x971add32ea87f10bd192671630be3be8a11b8623"
    pool_address1_query = "quote_token_price_base_token"
    pool_address1_name = "CRV / cvxCRV"
    crossing_up_price = 0.94
    crossing_down_price = 0.89

    datasource = Geckoterminal({pool_address1: pool_address1_query})
    tracker = TokenTracker(datasource)
    tracker.attach(watcher)

    high_processor = SimpleProcessor(
        crossing_up_price, SimpleProcessor.Condition.GREATER_OR_EQUAL
    )
    high_checker = CheckerHandler(pool_address1_name, high_processor, messengers)
    tracker.attach(high_checker)

    low_processor = SimpleProcessor(
        crossing_down_price, SimpleProcessor.Condition.LESS_OR_EQUAL
    )
    low_checker = CheckerHandler(pool_address1_name, low_processor, messengers)
    tracker.attach(low_checker)
    tracker.fetch()

    assert tracker.tokens[pool_address1_name].price
