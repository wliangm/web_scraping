from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


# Function to scrape Mars weather from Twitter
def scrape_mars_weather():

    # Initialize browser
    browser = init_browser()

    # Visit twitter for mars weather
    mars_tw_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_tw_url)
    
    #set timer and delay for 5 seconds before scrape the page
    time.sleep(5)

    # Scrape page into soup
    mars_tw_html = browser.html
    mars_tw_soup = BeautifulSoup(mars_tw_html , "html.parser")
    
    # Find today's forecast
    mars_tw_source_elem = mars_tw_soup.select_one("div.content div.js-tweet-text-container")
    mars_weather = mars_tw_source_elem.find("p", class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather_text = mars_weather.get_text()
        
    # Store in dictionary
    #mars_weather = {
    #    "weather": mars_weather_text
    #}
    
    #close browser
    browser.quit()

    # Return results
    return mars_weather_text





# Function to scrape Mars news from NASA
def scrape_mars_news():

    # Initialize browser
    browser = init_browser()

    # Visit NASA News site
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    
    #set timer and delay for 5 seconds before scrape the page
    time.sleep(5)

    # Scrape page into soup
    nasa_html = browser.html
    nasa_news_soup = BeautifulSoup(nasa_html, 'html.parser')

    # Find Title and Teaser paragraph
    nasa_slide_elem = nasa_news_soup.select_one('ul.item_list li.slide')
    
    news_list_text = nasa_slide_elem.find("div", class_='list_text')

    news_title = news_list_text.find("div", class_='content_title')
    news_teaser = news_list_text.find("div", class_='article_teaser_body')

    news_title_text = news_title.get_text()
    news_teaser_text = news_teaser.get_text()

    # Store in dictionary
    nasa_mars_news = {"news_title": news_title_text, "news_teaser": news_teaser_text}
    
    #close browser
    browser.quit()

    # Return results
    return nasa_mars_news



# Function to scrape Mars facts from space-facts.com
#def scrape_mars_facts():

    # use pandas to scrape tha facts table
#    mars_facts_url = 'http://space-facts.com/mars/'
    
    #set timer and delay for 5 seconds before scrape the page
#    time.sleep(5)
    
#    mars_facts_tables = pd.read_html(mars_facts_url)
    
    #convert the list to pd
#    mars_facts_df = mars_facts_tables[0]
#    mars_facts_df.columns = ['0','1']

    #rename header and reset index and remove index name
#    mars_facts_df = mars_facts_df.rename(columns= {'0':'Mars_Profile','1':'Mars_Profile_Measurement'})
#    mars_facts_df.set_index('Mars_Profile',inplace=True)
#    mars_facts_df.index.name = None ##'mars_profile'
    
    # Use Pandas to convert the data to a HTML table string.
#    mars_html_table = mars_facts_df.to_html()
#    mars_html_table.replace('\n', '')
    
#    mars_facts_df.to_html('mars_facts_table.html')
    
    # Return results
#    return mars_html_table

# Function to scrape Mars facts from space-facts.com
def mars_facts():
    try:
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        return None

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)
    ##df.index.name = None

    # Add some bootstrap styling to <table>
    return df.to_html()

    


# Function to scrape Mars main/featured image from JPL site
def scrape_mars_main_image():
    
    # Initialize browser
    browser = init_browser()

    # Visit JPL site
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    
    # Navigate to the source image page
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    browser.click_link_by_partial_href('/spaceimages/')
    time.sleep(5)

    # Scrape page into soup
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    # Find image url
    img_source_elem = jpl_soup.select_one('img')
    jpl_img_url = img_source_elem["src"]
    
    # Store in dictionary
    #jpl_mars_img = {"jpl_img_url": jpl_img_url}
    
    #close browser
    browser.quit()

    # Return results
    return jpl_img_url 



# Function to scrape Mars Hemispheres for title and image url from Astro site
def scrape_mars_hem_img():
    
    # Initialize browser
    browser = init_browser()

    # Visit Astro site
    mars_astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_astro_url)
    
    time.sleep(5)
    
    # Scrape page into soup
    mars_astro_html = browser.html
    mars_astro_soup = BeautifulSoup(mars_astro_html, 'html.parser')

    # Find hemisphere title and use for "for loop" later
    mars_astro_source_elem = mars_astro_soup.select('h3')
    
    #create two empty lists and dictionary
    hem_title_list = []
    hem_url_list = []
    mars_hem_title_url = []

    #start for loop to get each hemispheres's title and url
    for title in mars_astro_source_elem:
        #get text for each title from h3 list
        title_text = title.get_text()
        #append each title into title list
        hem_title_list.append(title_text)
        
        #begin scrapping,  click each title for each hemispheres per title
        browser.find_by_text(title_text).double_click()
        
        time.sleep(5)
        
        #convert the browser html to a soup object
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
        #find element for image download
        image_source_elem = image_soup.select_one('div.downloads')
        #find url from image download
        img_target = image_source_elem.find("a")
        #get url from href
        img_url = img_target['href']
        #append url into url list
        hem_url_list.append(img_url)
        
        #create dictionary for each combination of title and url
        mars_hem_dict = {'title': title_text,'url': img_url}
        #append each dictionary into final list
        mars_hem_title_url.append(mars_hem_dict)
        
        #return to main page for for-loop
        browser.visit(mars_astro_url)
        time.sleep(5)

        
    #close browser
    browser.quit()

    # Return results
    return mars_hem_title_url


