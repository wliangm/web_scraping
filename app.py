# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_info

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    weather = scrape_info.scrape_mars_weather()
    news = scrape_info.scrape_mars_news()
    #facts = scrape_info.scrape_mars_facts()
    facts = scrape_info.mars_facts()
    main_img = scrape_info.scrape_mars_main_image()
    hem_title_url = scrape_info.scrape_mars_hem_img()

    # Store results into a dictionary
    mars_dict = {
        "weather": weather,
        "news_title": news["news_title"],
        "news_teaser": news["news_teaser"],
        "facts_table": facts,
        "main_img_url": main_img,
        "hem_img": hem_title_url
        }

    # Insert mars into database
    mongo.db.collection.insert_one(mars_dict)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
