from typing import Dict

from cuckoo.base import DataSource, Token


class Geckoterminal(DataSource):
    # Setting datasource name
    name = "geckoterminal"
    # Setting query address and attribute of return, address:attribute
    parameter: Dict[str, str]

    def __init__(self, parameter: Dict[str, str]) -> None:
        super().__init__(Geckoterminal.name, 30)
        self.parameter = parameter

    def query(self) -> Dict[str, Token]:
        tokens = {}
        for address, attribute in self.parameter.items():
            response = self.request_helper.request(
                f"https://api.geckoterminal.com/api/v2/networks/eth/pools/{address}"
            )
            attributes = response["data"]["attributes"]
            symbol = attributes["name"]
            value = float(attributes[attribute])
            tokens[symbol] = Token(symbol, value)
        return tokens
