import requests

def get_items():
    payload = {"operationName":"fetchExploreData","variables":{},"query":"query fetchExploreData {\n  funds {\n    express {\n      amount\n      rate\n      max\n      __typename\n    }\n    expressStripe {\n      amount\n      rate\n      max\n      __typename\n    }\n    expressCrypto {\n      amount\n      rate\n      max\n      __typename\n    }\n    b4tax {\n      amount\n      rate\n      max\n      __typename\n    }\n    b4taxStripe {\n      amount\n      rate\n      max\n      __typename\n    }\n    b4taxCrypto {\n      amount\n      rate\n      max\n      __typename\n    }\n    hasWallet\n    __typename\n  }\n  recentlySold {\n    name\n    itemId\n    image\n    price\n    __typename\n  }\n  items {\n    itemId\n    name\n    image\n    rap\n    value\n    price\n    optimizedPrice\n    sellerFee\n    type\n    purchaseToken\n    paymentMethods {\n      name\n      data\n      __typename\n    }\n    seller {\n      id\n      username\n      __typename\n    }\n    hasPriceNotifier\n    isInUserWishlist\n    hasWallet\n    __typename\n  }\n}"}
    url = 'https://api.ro.place/graphql'

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['data']['items']
    print(f"Error: {response.status_code}, {response.text}")


def find_robux_dollar_ratio(items, calculation_type: int = 1):
    # Calculation mode either 1 or 2, 1 calculates the ratio based on the RAP while 2 calculates the ratio based on the value
    ratios = []
    for item in items:
        itemdata = {}
        itemdata['name'] = item['name']
        itemdata['rap'] = item['rap']
        itemdata['value'] = item['value']
        itemdata['price'] = item['price']
        itemdata['id'] = item['purchaseToken']
        itemdata['fee'] = item['sellerFee']
        # item['optimizedPrice'] = item['optimizedPrice']
        if calculation_type == 1:
            itemdata['ratio'] = (item['price'] / item['rap']) * 1000
        elif calculation_type == 2:
            itemdata['ratio'] = (item['price'] / item['value']) * 1000
        itemdata['ratio'] = round(itemdata['ratio'], 2)
        itemdata['price'] = round(itemdata['price'], 2)
        itemdata['mode'] = calculation_type
        ratios.append(itemdata)
    ratios.sort(key=lambda x: x['ratio'])
    return ratios

data = get_items()
ratios = find_robux_dollar_ratio(data)

with open('/Users/ttc/Downloads/roplaceratios.txt', 'w') as f:
    for item in ratios:
        fee_message = f"with the seller's fee of ${item['fee']}" if item['fee'] > 0 else "with no seller fee"
        f.write(f"[{item['name']}](<https://ro.place/item/{item['id']}>) - ${item['ratio']}/1000 Robux (R${item['rap'] if item['mode'] == 1 else item['value']} for ${item['price']} {fee_message})\n")