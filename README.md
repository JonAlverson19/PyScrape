# PyScrape
Scraper for Twitter built using the Twitter API for python hosted on a Flask app.

This program requires basic knowledge of flask in order to run the flask_interaction.py file and host the app. App will not run unless an external file called 'twitter_credentials.json' is included with a json object that contains the CONSUMER_SECRET, ACCESS_TOKEN, CONSUMER_KEY, and ACCESS_SECRET values given by twitter.

Once running, the app only needs the twitter handle before it scrapes for information including: display name, date account was created, the profile image, the banner image, follower handles, handles of people user follows, and status ids.
