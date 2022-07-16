
#import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

#getting api_token
iex_api_key = os.getenv('IEX_API_KEY')


def api_url(ticker):

    #creating the api_url
    base_URL = "https://cloud.iexapis.com/"
    version = "stable/"
    endpoint_path = f"stock/{ticker}/quote/"
    query_string = f"token={iex_api_key}"

    return f"{base_URL}{version}{endpoint_path}?{query_string}"

def get_latest_updates(*symbols):
    
    # iterating through each symbol
    for i in symbols:
        ticker = i
        
        # making a request
        r = requests.get(api_url(ticker))
        
        # converting a JSON response to a dict
        df = r.json()

        # printing
        print(df)

def main():
    get_latest_updates('TSLA')

main()
