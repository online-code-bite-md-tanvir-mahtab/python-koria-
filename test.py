from lib2to3.pgen2 import driver
from seleniumwire.undetected_chromedriver import webdriver
import undetected_chromedriver as webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

import pandas  as pd
import os
import datetime
print('hello world')


def collect_data(search_key):
    for i in range(1,2):
        web_site_urld_endpoint = f'https://www.coupang.com/np/search?q={search_key}&channel=auto&page={i}'
        option = Options()
        option.headless = True
        driver = webdriver.Chrome(options=option)

        driver.get(url=web_site_urld_endpoint)

        html_page = driver.page_source
        driver.close()

        soup = BeautifulSoup(html_page,'html.parser')
        for product_item in soup.find('ul',id='productList').find_all('li'):
            try:
                product_name = (product_item.find('div',class_='name').text)
            except:
                product_name = " "
            try:
                product_price = (product_item.find('strong',class_='price-value').text).split(',')
                product_price =  int(''.join(product_price))
            except:
                product_price = 0
            try:
                product_rating = float(product_item.find('em',class_='rating').text)
            except:
                product_rating = 0.0
            try:
                image_link = product_item.find('img', class_='search-product-wrap-img').get('src')
                product_image = f"https:{image_link}"
            except:
                product_image = " "
            product_revenue = product_item.find('div',class_='reward-cash-badge__inr').text.split(" ")[2].split('원')[0].split(',')
            try:
                product_revenue = pd.to_numeric(''.join(product_revenue))
            except:
                product_revenue =''.join(product_revenue)
            product_weekly_price = int(product_price * 7)
            product_monthly_price = int(product_price * 30)
            data = pd.read_csv('product_research.csv')

            df = pd.DataFrame({
                    'name':[product_name],
                    'price':[product_price],
                    'review':[product_rating],
                    'revenue':[product_revenue],
                    'weekly_price':[product_weekly_price],
                    'monthly_price':[product_monthly_price],
                    'img':[product_image]
                })
            print(df)



if __name__ == '__main__':
    collect_data('spoon')

# https://github.com/analyticalnahid/Machine-Learning-Roadmap?fbclid=IwAR0QHNQqIqf3hGvdhZCUKF4QfyPFWkHu_hhgr2KjuYvbY0c_8M9iz3Q-8vw TODO:
