from flask import Flask
from modules import scrape, clean, extract
import datetime as dt
import pandas as pd


app = Flask(__name__)
sentiment = 0

@app.route("/sentiment_update")
def sentiment_update():
  df = scrape.scrapeToday()
  df = clean.cleanTweets(df)
  df = extract.extractSentiment(df)
  df = extract.extractWeightedSentiment(df)

  sentiment = df.iloc[0]["weighted_sentiment"]

  return "<p>" + str(sentiment) + "</p>"