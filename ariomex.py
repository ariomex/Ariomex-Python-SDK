import hashlib
import json
import requests
import time
import hmac


class Ariomex:
    def __init__(self, api_key="", api_secret=""):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = "https://api.ariomex.com"
        self.general = General(self)
        self.account = Account(self)
        self.wallet = Wallet(self)
        self.bank = Bank(self)
        self.history = History(self)
        self.order = Order(self)

    def sign_and_send(self, url, query, method="GET", is_private=False):
        query["timestamp"] = str(round(time.time() * 1000))
        query_string = "&".join(f"{k}={v}" for k, v in query.items())
        if is_private:
            self.signature = hmac.new(
                self.api_secret.encode("utf-8"),
                query_string.encode("utf-8"),
                digestmod=hashlib.sha256,
            ).hexdigest()
        full_url = f"{self.api_url}{url}"
        if method not in ("GET", "DELETE"):
            request_data = json.dumps(query)
        else:
            full_url += f"?{query_string}"
            request_data = None

        return self.send_request(full_url, method, is_private, request_data)

    def send_request(self, url, method, is_private=False, request_data=None):
        headers = {"Content-Type": "application/json"}
        if is_private:
            headers["X-ARX-APIKEY"] = self.api_key
            headers["X-ARX-SIGNATURE"] = self.signature

        response = requests.request(method, url, headers=headers, data=request_data)
        return response.text


class General:
    def __init__(self, parent):
        self.parent = parent

    def swagger(self):
        url = "/v1/public/swagger"
        is_private_endpoint = False
        method = "GET"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def ping(self):
        url = "/v1/public/ping"
        is_private_endpoint = False
        method = "GET"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def time(self):
        url = "/v1/public/time"
        is_private_endpoint = False
        method = "GET"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def exchange_info(self, symbol=""):
        url = "/v1/public/exchange_info"
        is_private_endpoint = False
        method = "GET"
        query = {}
        if symbol != "":
            query["symbol"] = symbol
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def coins_info(self, symbol=""):
        url = "/v1/public/coins_info"
        is_private_endpoint = False
        method = "GET"
        query = {}
        if symbol != "":
            query["symbol"] = symbol
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def orderbook(self, symbol=""):
        url = "/v1/public/orderbook"
        is_private_endpoint = False
        method = "GET"
        query = {}
        if symbol != "":
            query["symbol"] = symbol
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def last_trades(self, symbol=""):
        url = "/v1/public/last_trades"
        is_private_endpoint = False
        method = "GET"
        query = {}
        if symbol != "":
            query["symbol"] = symbol
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def last_prices(self, symbol=""):
        url = "/v1/public/last_prices"
        is_private_endpoint = False
        method = "GET"
        query = {}
        if symbol != "":
            query["symbol"] = symbol
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def candlesticks(self, symbol, resolution, from_="", to=""):
        url = "/v1/public/candlesticks"
        is_private_endpoint = False
        method = "GET"
        query = {"symbol": symbol, "resolution": resolution}
        if from_ != "":
            query["from"] = from_
        if to != "":
            query["to"] = to
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)


class Account:
    def __init__(self, parent):
        self.parent = parent

    def get_account_info(self):
        url = "/v1/private/account/info"
        is_private_endpoint = True
        method = "GET"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_balance(self):
        url = "/v1/private/account/get_balance"
        is_private_endpoint = True
        method = "GET"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_dust_balance(self):
        url = "/v1/private/account/get_dust_balance"
        is_private_endpoint = True
        method = "GET"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def convert_dust_balance(self, coins_list):
        url = "/v1/private/account/convert_dust_balance"
        is_private_endpoint = True
        method = "POST"
        query = {"coinsList": coins_list}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)


class Wallet:
    def __init__(self, parent):
        self.parent = parent

    def generate_deposit_address(self):
        url = "/v1/private/wallet/generate_deposit_address"
        is_private_endpoint = True
        method = "POST"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_deposit_address(self):
        url = "/v1/private/wallet/get_deposit_address"
        is_private_endpoint = True
        method = "GET"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def withdraw_irt(self, amount, iban_uuid):
        url = "/v1/private/wallet/withdraw_irt"
        is_private_endpoint = True
        method = "POST"
        query = {"amount": amount, "iban_uuid": iban_uuid}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def withdraw_crypto(self, symbol, network, amount, address, memo=""):
        url = "/v1/private/wallet/withdraw_crypto"
        is_private_endpoint = True
        method = "POST"
        query = {
            "symbol": symbol,
            "network": network,
            "amount": amount,
            "address": address,
            "memo": memo,
        }
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_withdraw_addresses(self):
        url = "/v1/private/wallet/get_withdraw_address"
        is_private_endpoint = True
        method = "GET"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)


class Bank:
    def __init__(self, parent):
        self.parent = parent

    def set_bank_card(self, card_number):
        url = "/v1/private/bank/set_card"
        is_private_endpoint = True
        method = "POST"
        query = {"cardNumber": card_number}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def set_bank_iban(self, iban):
        url = "/v1/private/bank/set_iban"
        is_private_endpoint = True
        method = "POST"
        query = {"iban": iban}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_bank_accounts(self):
        url = "/v1/private/bank/get_accounts"
        is_private_endpoint = True
        method = "GET"
        query = {}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)


class History:
    def __init__(self, parent):
        self.parent = parent

    def get_irt_deposits(
        self, from_="", to="", status="", page="", max_rows_per_page=""
    ):
        url = "/v1/private/history/deposit/irt"
        is_private_endpoint = True
        method = "GET"
        query = {
            "from": from_,
            "to": to,
            "status": status,
            "page": page,
            "maxRowsPerPage": max_rows_per_page,
        }
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_crypto_deposits(
        self,
        symbol="",
        network="",
        from_="",
        to="",
        status="",
        page="",
        max_rows_per_page="",
    ):
        url = "/v1/private/history/deposit/crypto"
        is_private_endpoint = True
        method = "GET"
        query = {
            "symbol": symbol,
            "network": network,
            "from": from_,
            "to": to,
            "status": status,
            "page": page,
            "maxRowsPerPage": max_rows_per_page,
        }
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_irt_withdrawals(
        self, from_="", to="", status="", page="", max_rows_per_page=""
    ):
        url = "/v1/private/history/withdrawals/irt"
        is_private_endpoint = True
        method = "GET"
        query = {
            "from": from_,
            "to": to,
            "status": status,
            "page": page,
            "maxRowsPerPage": max_rows_per_page,
        }
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_crypto_withdrawals(
        self,
        symbol="",
        network="",
        from_="",
        to="",
        status="",
        page="",
        max_rows_per_page="",
    ):
        url = "/v1/private/history/withdrawals/crypto"
        is_private_endpoint = True
        method = "GET"
        query = {
            "symbol": symbol,
            "network": network,
            "from": from_,
            "to": to,
            "status": status,
            "page": page,
            "maxRowsPerPage": max_rows_per_page,
        }
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_orders(
        self,
        symbol="",
        orderId="",
        from_="",
        to="",
        type_="",
        side="",
        status="",
        page="",
        max_rows_per_page="",
    ):
        url = "/v1/private/history/orders"
        is_private_endpoint = True
        method = "GET"
        query = {
            "symbol": symbol,
            "orderId": orderId,
            "type": type_,
            "side": side,
            "from": from_,
            "to": to,
            "status": status,
            "page": page,
            "maxRowsPerPage": max_rows_per_page,
        }
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def get_trades(
        self,
        symbol="",
        from_="",
        to="",
        side="",
        page="",
        max_rows_per_page="",
    ):
        url = "/v1/private/history/trades"
        is_private_endpoint = True
        method = "GET"
        query = {
            "symbol": symbol,
            "side": side,
            "from": from_,
            "to": to,
            "page": page,
            "maxRowsPerPage": max_rows_per_page,
        }
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)


class Order:
    def __init__(self, parent):
        self.parent = parent

    def set_limit_buy(self, symbol, price, volume):
        url = "/v1/private/order/limit/buy"
        is_private_endpoint = True
        method = "POST"
        query = {"symbol": symbol, "price": price, "volume": volume}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def set_limit_sell(self, symbol, price, volume):
        url = "/v1/private/order/limit/sell"
        is_private_endpoint = True
        method = "POST"
        query = {"symbol": symbol, "price": price, "volume": volume}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def set_market_buy(self, symbol, total):
        url = "/v1/private/order/market/buy"
        is_private_endpoint = True
        method = "POST"
        query = {"symbol": symbol, "total": total}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def set_market_sell(self, symbol, volume):
        url = "/v1/private/order/market/sell"
        is_private_endpoint = True
        method = "POST"
        query = {"symbol": symbol, "volume": volume}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def set_sltp(self, symbol, volume, sl_price, tp_price):
        url = "/v1/private/order/sltp/sl_tp"
        is_private_endpoint = True
        method = "POST"
        query = {
            "symbol": symbol,
            "volume": volume,
            "sl_price": sl_price,
            "tp_price": tp_price,
        }
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def set_sl(self, symbol, volume, sl_price):
        url = "/v1/private/order/sltp/sl"
        is_private_endpoint = True
        method = "POST"
        query = {"symbol": symbol, "volume": volume, "sl_price": sl_price}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def set_stoplimit_buy(self, symbol, volume, price, stop_price):
        url = "/v1/private/order/stoplimit/buy"
        is_private_endpoint = True
        method = "POST"
        query = {"symbol": symbol, "volume": volume, "price": price, "stop": stop_price}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def set_stoplimit_sell(self, symbol, volume, price, stop_price):
        url = "/v1/private/order/stoplimit/sell"
        is_private_endpoint = True
        method = "POST"
        query = {"symbol": symbol, "volume": volume, "price": price, "stop": stop_price}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def cancel_order(self, symbol, order_uuid):
        url = "/v1/private/order/cancel"
        is_private_endpoint = True
        method = "DELETE"
        query = {"symbol": symbol, "order_uuid": order_uuid}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)

    def cancel_all_orders(self, symbol=""):
        url = "/v1/private/order/cancel_all"
        is_private_endpoint = True
        method = "DELETE"
        query = {"symbol": symbol}
        return self.parent.sign_and_send(url, query, method, is_private_endpoint)
