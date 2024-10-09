import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def get_data():
    options = Options()
    options.add_argument('--headless')
    options.set_preference('devtools.jsonview.enabled', False)
    browser = webdriver.Firefox(options=options)
    browser.get('https://adurite.com/api/market/roblox')

    data = browser.find_element(By.TAG_NAME, 'pre').text
    browser.quit()
    return json.loads(data)['items']['items'].values()


def find_robux_dollar_ratio(items):
    ratios = []
    for item in items:
        if item['paypal'] != '1' or item['stripe'] != '1':
            pass
        item_name = item['limited_name']
        seller_name = item['seller_name']
        rap = int(item['rap'])
        try:
            price = float(item['numeric_price'])
        except KeyError:
            price = int(item['price'].replace(',', ''))
        # Find the price per 1000 robux
        ratio = (price / rap) * 1000
        item_details = {
            'item_name': item_name,
            'seller_name': seller_name,
            'ratio': ratio,
            'rap': rap,
            'price': price
        }
        ratios.append(item_details)
    ratios.sort(key=lambda x: x['ratio'])
    return ratios

with open('limited_ratios.txt', 'w') as f:
    ratios = find_robux_dollar_ratio(get_data())
    for ratio in ratios:
        newratio = round(ratio['ratio'] * 100) / 100
        newprice = round(ratio['price'] * 100) / 100
        f.write(f"{ratio['item_name']} - [{ratio['seller_name']}](<https://adurite.com/shop/{ratio['seller_name']}>) - ${newratio}/1000 Robux - R${ratio['rap']} for ${newprice}\n")