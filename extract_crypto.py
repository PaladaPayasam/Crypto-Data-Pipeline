import datetime
import pandas as pd
import requests

def fetch_crypto_data():
    url="https://api.coingecko.com/api/v3/coins/markets"
    params={
        "vs_currency":"inr",
        "ids":"bitcoin,solana,ethereum,binancecoin",
        "order":"market_cap_desc",
        "per_page":100,
        "page":1,
        "sparkline":False
    }
    
    print("Fetching data from CoinGecko API...")
    
    try:
        response=requests.get(url,params=params)
        response.raise_for_status()
        data=response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
    extracted_data=[]
    for coin in data:
        record={
            "extracted_at": datetime.datetime.now().isoformat(),
            "coin_id": coin.get("id"),
            "symbol": coin.get("symbol").upper() if coin.get("symbol") else None,
            "name": coin.get("name"),
            "current_price": coin.get("current_price"),
            "market_cap": coin.get("market_cap"),
            "total_volume": coin.get("total_volume"),
            "price_change_percentage_24h": coin.get("price_change_percentage_24h"),
        }
        extracted_data.append(record)
        
    df = pd.DataFrame(extracted_data)
    return df


if __name__ == "__main__":
    crypto_df = fetch_crypto_data()
    
    if crypto_df is not None and not crypto_df.empty:
        print("Data fetched successfully:")
        print(crypto_df.head())
        
        crypto_df.to_csv("crypto_data.csv", index=False)
        print("Data saved to crypto_data.csv")
    else:
        print("No data to save.")