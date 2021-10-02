from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd


def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit NASA Mars News website
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # visit JPL Mars Space Images website

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find('img', class_='thumbimg')
    img_src = image['src']
    featured_image_url = url + img_src

    # visit Mars Facts website

    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    mars_data = tables[0]
    new_header = mars_data.iloc[0]
    mars_data = mars_data[1:]
    mars_data.columns = new_header
    mars_data = mars_data.set_index("Mars - Earth Comparison")

    mars_table = mars_data.to_html()

    # visit Mars Hemispheres website

    url = 'https://marshemispheres.com/'
    browser.visit(url)    
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_='description')

    hemisphere_image_urls = []

    for result in results:
        

        #find the title and href and add it to the base url
        title = result.h3.text
        href = result.find('a')['href']
        temp_url = url + href
        
        # go to temp url and find high res image link
        browser.visit(temp_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        image_src = soup.find('img', class_="wide-image")['src']
        image_url = url + image_src


        temp_dict = {}
        temp_dict['title'] = title
        temp_dict['img_url'] = image_url
        hemisphere_image_urls.append(temp_dict)

        mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_table" : str(mars_table),
            "hemisphere_image_urls": hemisphere_image_urls
        }

    browser.quit()
    print(mars_dict)

    return mars_dict