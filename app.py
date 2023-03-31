from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_page(url, max_price):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the section header
    section_header = soup.find('h2', class_='banner-title').text.strip()

    # Find all divs with class 'product-name' and 'product-price'
    divs = soup.find_all('div', class_='product-name')
    prices = soup.find_all('div', class_='product-price')

    # Check product price for each div and store products within the specified price range
    products = []
    for i in range(len(divs)):
        product_name = divs[i].find('a').text.strip()
        product_price = float(prices[i].text.strip().replace(',', ''))
        if product_price <= max_price:
            products.append({'name': product_name, 'price': product_price})

    return {'header': section_header, 'products': products}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        max_price = float(request.form['max_price'])

        urls = [
            "https://cafejavas.co.ug/user/productOrder/NTk=/MjIz/STARTERS%20AND%20APPETIZERS?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjI3/SANDWICHES?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjUw/CHICKEN?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MzIx/BIG%20MEAL%20COMBOS?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjI0/BITS%20&%20BITES?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjI2/SALADS?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjI1/SOUPS?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjI4/BURGERS?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjUx/FISH?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjUy/BEEF?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjUz/CURRIES?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjU1/PASTA?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjU2/MEX-FIX?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjU3/PIZZA?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MjU5/KIDDIE%20MEALS?cat=GENEROUS%20BIG%20MEALS",
    "https://cafejavas.co.ug/user/productOrder/NTk=/MzE0/Extras?cat=GENEROUS%20BIG%20MEALS"
        ]

        results = []
        for url in urls:
            results.append(scrape_page(url, max_price))

        return render_template('results.html', results=results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

