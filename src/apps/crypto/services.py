from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

import requests
from requests.exceptions import HTTPError, RequestException, Timeout

from apps.common.exceptions import BadGatewayException, InternalServerException
from apps.crypto.enum import Currency
from apps.crypto.types import CryptoBitcoinPriceType


class CryptoBitcoinService:
    def get_bitcoin_price(self, currency: Currency) -> float:
        url = "https://blockchain.info/ticker"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if currency.value not in data:
                raise BadGatewayException(
                    f"Currency '{currency.value}' not found in the Bitcoin price response."
                )
            return float(data[currency.value]["last"])
        except (HTTPError, RequestException, Timeout) as e:
            raise BadGatewayException(f"Failed to fetch Bitcoin price: {e}") from e
        except KeyError as e:
            raise InternalServerException(
                f"Invalid structure in Bitcoin price response for currency '{currency.value}'."
            ) from e
        except Exception as e:
            raise InternalServerException(f"Something went wrong: {e}") from e

    def get_exchange_rate(self, base_currency: Currency, target_currency: Currency, month: str) -> float:
        url = f"https://data-api.ecb.europa.eu/service/data/EXR/M.{target_currency.value}.{base_currency.value}.SP00.A?startPeriod={month}&endPeriod={month}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.text)
            obs_value = root.find(
                ".//{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}ObsValue"
            )
            if obs_value is None or "value" not in obs_value.attrib:
                raise BadGatewayException(
                    f"Exchange rate data not found for {base_currency.value} to {target_currency.value} in {month}."  # noqa: E501
                )
            return float(obs_value.attrib["value"])
        except (HTTPError, RequestException, Timeout) as e:
            raise BadGatewayException(f"Failed to fetch exchange rate: {e}") from e
        except ET.ParseError as e:
            raise InternalServerException("Failed to parse XML response from exchange rate API.") from e
        except Exception as e:
            raise InternalServerException(f"Something went wrong: {e}") from e

    def calculate_bitcoin_price_from_exchange_rate(self, exchange_rate: float, bitcoin_price: float) -> float:
        try:
            return bitcoin_price * exchange_rate
        except TypeError as e:
            raise IndentationError(
                "Invalid input types for calculating Bitcoin price from exchange rate."
            ) from e
        except Exception as e:
            raise InternalServerException(f"Something went wrong: {e}") from e

    def get_bitcoin_data(self) -> CryptoBitcoinPriceType:
        last_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
        bitcoin_eur_price = self.get_bitcoin_price(Currency.EUR)
        eur_to_gbp_rate = self.get_exchange_rate(
            base_currency=Currency.EUR, target_currency=Currency.GBP, month=last_month
        )
        bitcoin_gbp_price = self.calculate_bitcoin_price_from_exchange_rate(
            exchange_rate=eur_to_gbp_rate, bitcoin_price=bitcoin_eur_price
        )
        return CryptoBitcoinPriceType(
            bitcoin_eur=bitcoin_eur_price,
            eur_to_gbp=eur_to_gbp_rate,
            bitcoin_gbp=bitcoin_gbp_price,
        )
