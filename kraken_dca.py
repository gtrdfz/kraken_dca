import urllib.parse
import hashlib
import hmac
import base64
import time
import requests
import schedule
import datetime

# UPDATE WITH YOUR KRAKEN CREDENTIALS
api_key = ""
private_key = ""
pair = "XXBTZUSD" # BTC/USD
purchase_price = 10


def get_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def request(uri_path, data, public_key, api_sec):
    headers = {}
    headers['API-Key'] = public_key
    headers['API-Sign'] = get_signature(uri_path, data, api_sec)
    req = requests.post(("https://api.kraken.com" + uri_path), headers=headers, data=data)
    return req


def get_price(pair):
    resp = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={pair}').json()
    ask_price = resp['result'][pair]['a'][0]
    return float(ask_price)


def calculate_volume_from_price(price, pair) -> float:
    volume = price / get_price(pair)
    return volume


def buy_crypto():
    resp = request('/0/private/AddOrder', {
        "nonce": str(int(1000 * time.time())),
        "ordertype": "market",
        "type": "buy",
        "pair": pair,
        "volume": calculate_volume_from_price(purchase_price, pair),
    }, api_key, private_key)
    print(f"### Run at {datetime.datetime.now()}")
    print(resp.json())


print(f"### Script start at {datetime.datetime.now()}")
schedule.every().monday.at("14:00", "Europe/Amsterdam").do(buy_crypto) # UPDATE DCA SCHEDULE

while True:
    schedule.run_pending()
    time.sleep(1)
