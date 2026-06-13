from mage_ai.data_preparation.decorators import data_loader
import requests
import pandas as pd

@data_loader
def load_data_from_api(*args, **kwargs):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "inr",
        "ids": "bitcoin,ethereum,solana,cardano"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    return pd.DataFrame(data)[['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']]