import requests as req
import json
import uuid
from genhash import generate_signature, to_slug
import hashlib
from tqdm import tqdm
import pandas as pd

def searchZepto(query, storeId = "482b8c90-9e75-4390-9884-64f00a4ce22c" ):
#     url = "https://api.zepto.com:443/api/v3/search"
    url = "https://bff-gateway.zepto.com/user-search-service/api/v3/search"
    headers = {"X-Xsrf-Token": "2A3-0NT8FRxkA6roXxOve:6xIYDgOSc8c2zBUOAMz2KrG0-gU.N4vXaZjT5zeeilPgJlvXOVJJD++SysSFGaRhUfDjgBF", #Replace with your actual X-Xsrf-Token
               "Storeid": storeId,
               "Store_ids": storeId,
               "Request_id": "6b8d0bcc-29c4-4986-9c3e-a4e0e6bf76a1",
               "Appversion": "15.22.6",
               "Marketplace_type": "SUPER_SAVER",
               "Accept": "application/json, text/plain, */*",
               "Device_id": "b5ef7aee-9d66-412c-a84d-e5a7ffb6805d",
               "Content-Type": "application/json",
               "X-Csrf-Secret": "YPMgfs4f5mQ",
               "Platform": "WEB",
               "Accept-Language": "en-GB,en;q=0.9",
               "Tenant": "ZEPTO",
               "Auth_revamp_flow": "v2",
               "App_version": "12.77.1",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
               "App_sub_platform": "WEB",
               "Origin": "https://www.zepto.com",
               "Referer": "https://www.zepto.com/",
               "Accept-Encoding": "gzip, deflate, br",
               "Priority": "u=1, i"
              }
    responses = []

    pageNumber=0
    while True:
        print(f"Search Page Number: {pageNumber}", end = '\r')
        payload = json.dumps({"query":query,"pageNumber":pageNumber,"mode":"AUTOSUGGEST","intentId":str(uuid.uuid4()),"userSessionId":str(uuid.uuid4())},
                  separators=(',', ':'))

        config = {
                "method": "post",
                "url": "/api/v3/search",
                "baseURL": "https://bff-gateway.zepto.com/user-search-service/api/",
                "data": payload,
                "headers": {"request_id": headers['Request_id'], "device_id": headers['Device_id']}
                }
        secret = headers['X-Xsrf-Token']
        signature = generate_signature(config, secret)
        headers['Request-Signature'] = signature
        timezone = hashlib.sha256(signature.encode("utf-8")).hexdigest()
        headers['X-Timezone']=timezone
        out = req.post(url, headers=headers, data=payload)

        assert out.status_code == 200, (out.status_code, query, out.text)
        if out.json()['pageProductCount']==0:
            break
        responses.extend(out.json()['layout'])
        pageNumber+=1
    return responses


results= []
cats = ['ice cream', 'frozen food', 'chips']
storeId = "425e2ef0-02bc-4c87-b423-cfbc6e56984a" #Bangalore Whitefied

for cat in tqdm(cats):
    print(f"Searching: {cat}")
    products = searchZepto(cat, storeId)
    for i in products:
        if i ['widgetId'] == "PRODUCT_GRID":
            data = i['data']['resolver']['data']['items']
            for item in data:
                product = item['productResponse']
                product_info = product['product']
                variant = product['productVariant']
                slug = to_slug(product_info['name'])
                link = f"https://zepto.com/pn/{slug}/pvid/{variant['id']}"
                product_id = product_info['id']
                product_name = product_info['name']
                size = variant['formattedPacksize']
                mrp = product['mrp']
                final_price = product['discountedSellingPrice']
                discount_percent = product['discountPercent']

                results.append({
                        'name': product_name,
                        'size': size,
                        'mrp': mrp/100,
                        'final_price': final_price/100,
                        'discount_percent': discount_percent,
                        'link': link,
                        'category': cat
        })

df = pd.DataFrame(results).drop_duplicates(['link']).sort_values("discount_percent",ascending=False)
df=df.query("discount_percent>10")
print(df.to_string(index=False))