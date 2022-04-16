from crypt import methods
from urllib import response
from flask import Flask, jsonify
from modules import scrape, clean, extract, prediction, prediction_no_sentiment
import datetime as dt
import pandas as pd
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/update_sentiment")
def update_sentiment():
  df = scrape.scrapeToday()
  df = clean.cleanTweets(df)
  df = extract.extractSentiment(df)
  df = extract.extractWeightedSentiment(df)

  sentiment = df.iloc[0]["weighted_sentiment"]

  sentiment_json = {"sentiment": sentiment}

  with open('sentiment.json', 'w') as json_file:
    json.dump(sentiment_json, json_file)

  return jsonify(sentiment_json)

@app.route("/get_sentiment")
def get_sentiment():

  with open('sentiment.json') as json_file:
    sentiment_json = json.load(json_file)

  return jsonify(sentiment_json), 200

@app.route("/predict_with_sentiment")
def predict_with_sentiment():

  with open('sentiment.json') as json_file:
    sentiment_json = json.load(json_file)
  
  predicted_value = prediction.predict_to_string(sentiment_json["sentiment"])

  return jsonify({"predicted_value_with_sentiment": predicted_value})

@app.route("/predict_without_sentiment")
def predict_without_sentiment():
  predicted_value = prediction_no_sentiment.predict_to_string()

  return jsonify({"predicted_value_without_sentiment": predicted_value})

if __name__ == '__main__':
  app.run(host='0.0.0.0')