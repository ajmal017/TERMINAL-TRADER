import requests
from hashlib import sha512

def get_price(ticker):
#Gets current market price from cloud API based on inputted ticker.
    url = f"https://cloud.iexapis.com/stable/stock/{ticker.upper()}/quote?token=pk_0ccf442942da4ec98c6591dc520a3b84"
    response = requests.get(url)
    return response.json()["latestPrice"]

def hash_password(password, salt="salt"):
#Hashes entered password.
    hasher = sha512()
    hasher.update(password.encode() + salt.encode())
    return hasher.hexdigest()
