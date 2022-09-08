from operator import index
from sqlite3 import Row
from threading import Thread
from seleniumwire.undetected_chromedriver import webdriver
import undetected_chromedriver as webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import requests
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for, Response, stream_with_context
import datetime
import time
import json
import random
from datetime import datetime

'''this will collect all the data'''
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
            try:
                product_revenue = product_item.find('div',class_='reward-cash-badge__inr').text.split(" ")[2].split('원')[0].split(',')
                try:
                    product_revenue = pd.to_numeric(''.join(product_revenue))
                except:
                    product_revenue =''.join(product_revenue)
                
            except:
                product_revenue = 0

            product_weekly_price = int(product_price * 7)

            product_monthly_price = int(product_price * 30)


            data = pd.read_csv('product_research.csv')

            if data.empty:
                df = pd.DataFrame({
                    'name':[product_name],
                    'price':[product_price],
                    'review':[product_rating],
                    'revenue':[product_revenue],
                    'weekly_price':[product_weekly_price],
                    'monthly_price':[product_monthly_price],
                    'img':[product_image]
                })
                df.to_csv('product_research.csv',index=False,header=True)
            else:
                df = pd.DataFrame({
                    'name':[product_name],
                    'price':[product_price],
                    'review':[product_rating],
                    'revenue':[product_revenue],
                    'weekly_price':[product_weekly_price],
                    'monthly_price':[product_monthly_price],
                    'img':[product_image]
                })
                df.to_csv('product_research.csv',index=False,header=False,mode='a')


def add_to_the_table_for_tracking(web_url):
    web_site_endpoint = web_url
    option = Options()
    option.headless = True

    driver = webdriver.Chrome(options=option)

    driver.get(url=web_site_endpoint)



    html_page = driver.page_source

    driver.close()
    driver.quit()
    soup = BeautifulSoup(html_page,'html.parser')
    try:
        product_name = soup.find('h2',class_='prod-buy-header__title').text
    except:
        product_name = " "
    try:
        product_price = (soup.find('span',class_='total-price').text).split(" ")[0]
    except:
        product_price = 0
    try:
        product_sell = ((soup.find('span',class_='reward-cash-txt').text).split(" ")[28])
    except:
        product_sell = 0
    data = pd.read_csv('product_track.csv')
    import datetime
    time = datetime.datetime.now()
    time.strftime('%j:%m:%Y')
    if data.empty:
        df2 = pd.DataFrame({
            'name':[product_name],
            'file_name':[product_name],
            'price':[product_price],
            'sell':[product_sell],
            'time':[time],
            'url':[web_site_endpoint]
        })
        df2.to_csv("product_track.csv",index=False)
    else:
        df2 = pd.DataFrame({
            'name':[product_name],
            'file_name':[product_name],
            'price':[product_price],
            'sell':[product_sell],
            'time':[time],
            'url':[web_site_endpoint]
        })
        df2.to_csv('product_track.csv',mode='a',index=False,header=False)

def perform_to_collect_the_graph_data(index):
    url_data = pd.read_csv('product_track.csv')['url'][index]
    web_site_endpoint = url_data
    option = Options()
    option.headless = True

    driver = webdriver.Chrome(options=option)

    driver.get(url=web_site_endpoint)



    html_page = driver.page_source

    driver.close()
    driver.quit()
    soup = BeautifulSoup(html_page,'html.parser')
    try:
        product_name = soup.find('h2',class_='prod-buy-header__title').text
    except:
        product_name = " "
    try:
        product_price = (soup.find('span',class_='total-price').text).split()[0].split('원')[0].split(',')
        product_price = int(''.join(product_price))
    except:
        product_price = 0
    try:
        product_sell = ((soup.find('span',class_='reward-cash-txt').text).split(" ")[3])
    except:
        product_sell = 0
    time = datetime.now()
    time.strftime('%j:%m:%Y')
    df2 = pd.DataFrame({
        'name':[product_name],
        'price':[product_price],
        'sell':[product_sell],
        'time':[time]
    })
    return df2

'''it will show the data'''
def show_the_data(search_key):
    data = pd.read_csv('product_research.csv')
    if data.empty:
        t = Thread(target=collect_data,args=(search_key,))
        t.start()
        t.join()
        data = pd.read_csv('product_research.csv')
        return data
    else:
        if len(search_key) != 0:
            print(search_key)
            data  = pd.DataFrame({
                'name':[],
                'price':[],
                'review':[],
                'img':[]
            })
            data.to_csv('product_research.csv',index=False,header=False)
            return data
        else:
            return data






app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/research', methods=['GET','POST'])
def product_research():
    df =pd.read_csv('product_research.csv')
    # pd.cle
    index = len(df)
    if request.method == 'POST':
        s_k = request.form.get('c2')
        print(f'the value :{len(s_k)}')
        df2 = show_the_data(s_k)
        max_data = pd.to_numeric(request.form.get('maxPrice'))
        min_data = pd.to_numeric(request.form.get('minPrice'))
        max_review_data = pd.to_numeric(request.form.get('maxReview'))
        min_review_data = pd.to_numeric(request.form.get('minReview'))
        return render_template('product_research.html', data=df2, 
        i=index,max_value=(max_data),min_value=(min_data),
        max_review=(max_review_data), min_review=(min_review_data),enter=True)
    max_data = 0
    min_data = 0
    max_review_data = 0
    min_review_data = 0
    return render_template('product_research.html', data=df, 
    i=index,max_value=(max_data),min_value=(min_data),
    max_review=(max_review_data), min_review=(min_review_data),enter=False)
    

@app.route('/tracker', methods=['GET','POST'])
def product_tracker():
    if request.method == 'POST':
        add_to_the_table_for_tracking(request.form.get('url'))
        return redirect(url_for('product_tracker'))
    df = pd.read_csv('product_track.csv')
    index = len(df)

    return render_template('product_tracker.html', data=df,i=index)
# https://api.junglescout.com/api/products/get_products?skipCounter=true



@app.route('/graph/<int:index>')
def show_graph(index):
    return render_template('graph.html',id=index)

@app.route('/chart-data/<int:index>')
def chart_data(index):
    def generate_random_data():
        while True:
            df = perform_to_collect_the_graph_data(index)
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': int(df['price'][0])})
            yield f"data:{json_data}\n\n"

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response



@app.route('/delete/<int:index>')
def delete_product(index):
    data = pd.read_csv('product_track.csv')
    data.drop([index],axis=0,inplace=True)
    data.to_csv('product_track.csv')
    return redirect(url_for('product_tracker'))

if __name__ == '__main__':
    # collect_data()
    app.run(debug=True, threaded=True)