
import pandas as pd
import numpy as np
import requests
from pandas import json_normalize
import json

def safe_load_json(x):
    try:
        return json.loads(x)
    except (json.JSONDecodeError, TypeError):
        return None

def get_auctions():
    cookies = {
    '_ga': 'GA1.1.240731867.1710958850',
    'XSRF-TOKEN': 'eyJpdiI6Inhmc2NreTlsTXJJVGw3KzJTNmRMWEE9PSIsInZhbHVlIjoiWTRUbmZCcU5MaGtuaWZyaWEwbENhbWdKcHNtVTg2Y2dCcE02blRYbnhFMEpLQWc1YWwzaDA5UzJBN0Q0TkczdGduQURPUXI0WDU4bmpHdkZocThiNE41ek40ckZXRDViM2RWa2ppNFhaNXN2YzZWVFN3R29QV2JkK0pNUmo0WHoiLCJtYWMiOiJjMDU0N2I0Y2VhYTkzMmI4NmRkM2I3ODg5YzRjZWQyMTA0MzJlMzQwM2NlZTQ2NTU5ZDNmZWI5Yjc0YTk4MGU5In0%3D',
    'amx_session': 'eyJpdiI6IkFnclVPQ2hERG5mTUMzUmRKdm83b1E9PSIsInZhbHVlIjoiTVd0bmxvZ3BVTlZ5eFwvQVNUKzJrRVhiZVNKSzJUOVo0YVZGanVEd3ZGSDFVem4wVXVcL0d3SGwzaFptcXRlY1Z2R2FCS05VNjVKQ2pMeXdqTVB0RWFvajU4NVh6dGhzdUNJaFFBSEJMTGpySWg2MFFKQ0RPS2N1UWEyUHYrVzBRbyIsIm1hYyI6ImM0YTA5ZTYxYTQyM2NhM2Y4ZTdhYTgzNThmZjAyZDhlOGUwN2RjOGVkYzQ0MGI0YzExYThhODMwMmU0OTk5YzYifQ%3D%3D',
    '_ga_XFDNP90GQ4': 'GS1.1.1713511340.29.1.1713511663.0.0.0',
    }

    headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': '_ga=GA1.1.240731867.1710958850; XSRF-TOKEN=eyJpdiI6Inhmc2NreTlsTXJJVGw3KzJTNmRMWEE9PSIsInZhbHVlIjoiWTRUbmZCcU5MaGtuaWZyaWEwbENhbWdKcHNtVTg2Y2dCcE02blRYbnhFMEpLQWc1YWwzaDA5UzJBN0Q0TkczdGduQURPUXI0WDU4bmpHdkZocThiNE41ek40ckZXRDViM2RWa2ppNFhaNXN2YzZWVFN3R29QV2JkK0pNUmo0WHoiLCJtYWMiOiJjMDU0N2I0Y2VhYTkzMmI4NmRkM2I3ODg5YzRjZWQyMTA0MzJlMzQwM2NlZTQ2NTU5ZDNmZWI5Yjc0YTk4MGU5In0%3D; amx_session=eyJpdiI6IkFnclVPQ2hERG5mTUMzUmRKdm83b1E9PSIsInZhbHVlIjoiTVd0bmxvZ3BVTlZ5eFwvQVNUKzJrRVhiZVNKSzJUOVo0YVZGanVEd3ZGSDFVem4wVXVcL0d3SGwzaFptcXRlY1Z2R2FCS05VNjVKQ2pMeXdqTVB0RWFvajU4NVh6dGhzdUNJaFFBSEJMTGpySWg2MFFKQ0RPS2N1UWEyUHYrVzBRbyIsIm1hYyI6ImM0YTA5ZTYxYTQyM2NhM2Y4ZTdhYTgzNThmZjAyZDhlOGUwN2RjOGVkYzQ0MGI0YzExYThhODMwMmU0OTk5YzYifQ%3D%3D; _ga_XFDNP90GQ4=GS1.1.1713511340.29.1.1713511663.0.0.0',
    'Referer': 'https://amx.am/en/government_bond_auctions',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    }

    response = requests.get('https://amx.am/api/getGovernmentAuctions', cookies=cookies, headers=headers)
    data = response.json()['data']
    df = pd.DataFrame([data])
    df =df.melt()
    df.drop(columns = ['variable'], inplace = True)

    df['value'] = df['value'].astype(str)
    df['value'] = df['value'].str.replace("issuer's", 'issuer')
    df['value'] = df['value'].str.replace("'", '"')
    df['value'] = df['value'].str.replace("None", '"None"')
    df['value'] = df['value'].str.replace("False", '"False"')
    df['value'] = df['value'].str.replace("True", '"True"')

    df['value'] = df['value'].apply(safe_load_json)
    df= json_normalize(df['value'])

    r_d = {'1':'Allocation', '2':'Buyback', '3':'Additional Allocation'}
    df['auction_type_id'] = df['auction_type_id'].replace(r_d)

    df['yield'] = df['yield'].apply(lambda x: int(x.replace('.',''))/100)
    df['auction_yield'] = pd.to_numeric(df['auction_yield'], errors='coerce')

    df.rename(columns={'creation_date':'Announcement',
                  'auction_type_id':'Auction_Type',
                  'auction_code':'Auction_ID',
                  'yield':'Coupon',
                  'auction_yield':'Auction_Min_Yield',
                   'auction_percent':'Percent of Accepted Bids by Cut-Off Price',
                   'demand_quantity':'Amounts of the Total Bids',
                   'traded_quantity':'Amounts of the Total Accepted Bids'
                  }, inplace = True)
    
    df['auction_date'] = pd.to_datetime(df['auction_date']) 
    df['settlement_date'] = pd.to_datetime(df['settlement_date']) 
    df['issue_date'] = pd.to_datetime(df['issue_date']) 
    df['maturity_date'] = pd.to_datetime(df['maturity_date'])
    df['maturity_payment_date'] = pd.to_datetime(df['maturity_payment_date'])
    df['first_payment_date'] = pd.to_datetime(df['first_payment_date'])
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    df.drop(columns = ['instrument.cpn_frequency_ru', 'instrument.cpn_frequency', 'notes_ru', 'notes'], inplace = True)

    df['Coupon'] = pd.to_numeric(df['Coupon'], errors='coerce')
    df['issue_amount'] = pd.to_numeric(df['issue_amount'], errors='coerce')
    df['Auction_Min_Yield'] = pd.to_numeric(df['Auction_Min_Yield'], errors='coerce')
    df['minimum_amount'] = pd.to_numeric(df['minimum_amount'], errors='coerce')
    df['maximum_amount'] = pd.to_numeric(df['maximum_amount'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['Amounts of the Total Bids'] = pd.to_numeric(df['Amounts of the Total Bids'], errors='coerce')
    df['Amounts of the Total Accepted Bids'] = pd.to_numeric(df['Amounts of the Total Accepted Bids'], errors='coerce')
    df['average'] = pd.to_numeric(df['average'], errors='coerce')
    df['maximum'] = pd.to_numeric(df['maximum'], errors='coerce')
    df['minimum'] = pd.to_numeric(df['minimum'], errors='coerce')
    df['Percent of Accepted Bids by Cut-Off Price'] = pd.to_numeric(df['Percent of Accepted Bids by Cut-Off Price'], errors='coerce')
    df['waprice'] = pd.to_numeric(df['waprice'], errors='coerce')
    df['wayield'] = pd.to_numeric(df['wayield'], errors='coerce')
    df['maxprice'] = pd.to_numeric(df['maxprice'], errors='coerce')
    df['minprice'] = pd.to_numeric(df['minprice'], errors='coerce')
    df['wayield'] = pd.to_numeric(df['wayield'], errors='coerce')
    df['wayield'] = pd.to_numeric(df['wayield'], errors='coerce')

    df.drop(columns=['instrument.cpn_frequency_en', 'instrument.isin'], inplace =True)
    df['The volume of bonds to be auctioned'] = df.apply(lambda x: x['minimum_amount'] if pd.isnull(x['amount']) else x['amount'], axis = 1)
    df.to_excel(r'C:\Octo BI\FinSectorDaily\auction.xlsx', index=False)

def send_message(message_content):
    pass


if __name__ == '__main__':
    auctions = get_auctions()
    message_content = "Auction data updated"
    send_message(message_content)