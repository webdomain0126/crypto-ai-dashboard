<<<<<<< HEAD
import requests
import json


def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,dogecoin",
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params)
    return response.json()


def save_to_file(data, filename="crypto_data.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def print_summary(data):
    print("Crypto Prices Today:")
    print(f"Bitcoin: ${data['bitcoin']['usd']}")
    print(f"Ethereum: ${data['ethereum']['usd']}")

def print_summary(data):
    print("Crypto Prices Today:")
    print(f"Bitcoin: ${data['bitcoin']['usd']}")
    print(f"Ethereum: ${data['ethereum']['usd']}")
    print(f"Dogecoin: ${data['dogecoin']['usd']}")


if __name__ == "__main__":
    crypto_data = fetch_crypto_data()
    save_to_file(crypto_data)
=======
import requests
import json


def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,dogecoin",
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params)
    return response.json()


def save_to_file(data, filename="crypto_data.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def print_summary(data):
    print("Crypto Prices Today:")
    print(f"Bitcoin: ${data['bitcoin']['usd']}")
    print(f"Ethereum: ${data['ethereum']['usd']}")

def print_summary(data):
    print("Crypto Prices Today:")
    print(f"Bitcoin: ${data['bitcoin']['usd']}")
    print(f"Ethereum: ${data['ethereum']['usd']}")
    print(f"Dogecoin: ${data['dogecoin']['usd']}")


if __name__ == "__main__":
    crypto_data = fetch_crypto_data()
    save_to_file(crypto_data)
>>>>>>> 52712f6d46e41df808da5d751f28e415049ef994
    print_summary(crypto_data)