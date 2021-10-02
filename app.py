from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def home():
    mars_dict = mongo.db.collection.find_one()

    return render_template("index.html", mars=mars_dict)

@app.route('/scrape')
def scrape():
    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo db using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # redirect to the home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)