from crypt import methods
from urllib import response
from flask import Flask, Response, jsonify
from modules import scrape, clean, extract, prediction, prediction_no_sentiment
from datetime import datetime
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)



# @app.route("/update_sentiment")
# def update_sentiment():
#   df = scrape.scrapeToday()
#   df = clean.cleanTweets(df)
#   df = extract.extractSentiment(df)
#   df = extract.extractWeightedSentiment(df)

#   sentiment = df.iloc[0]["weighted_sentiment"]

#   sentiment_json = {"sentiment": sentiment}

#   with open('sentiment.json', 'w') as json_file:
#     json.dump(sentiment_json, json_file)

#   return jsonify(sentiment_json)



# @app.route("/get_sentiment")
# def get_sentiment():

#   with open('sentiment.json') as json_file:
#     sentiment_json = json.load(json_file)

#   return jsonify(sentiment_json), 200



# @app.route("/predict_with_sentiment")
# def predict_with_sentiment():

#   with open('sentiment.json') as json_file:
#     sentiment_json = json.load(json_file)
  
#   predicted_value = prediction.predict_to_string(sentiment_json["sentiment"])

#   return jsonify({"predicted_value_with_sentiment": predicted_value})



# @app.route("/predict_without_sentiment")
# def predict_without_sentiment():
#   predicted_value = prediction_no_sentiment.predict_to_string()

#   return jsonify({"predicted_value_without_sentiment": predicted_value})



@app.route("/get_predictions")
def update_predictions():
  df = pd.read_pickle("./data/predictions.pkl")
  pred_without_sentiment = prediction_no_sentiment.predict_to_string()
  res = df.head(10).to_json(orient="records")

  if (pred_without_sentiment == df.loc[0, "pred"]):
    res = df.head(10).to_json(orient="records")
  else:
    sentiment = get_sentiment()
    pred_with_sentiment = prediction.predict_to_string(sentiment)

    new_row = pd.DataFrame({
      "index": [df.shape[0]],
      "date": [datetime.now()],
      "sentiment": [sentiment], 
      "pred": [pred_without_sentiment], 
      "pred_sent": [pred_with_sentiment]
    })

    df = pd.concat([new_row, df], ignore_index=True)
    df.to_pickle("./data/predictions.pkl")
    res = df.head(10).to_json(orient="records")
  
  return Response(res, mimetype='application/json')

def get_sentiment():
  df = scrape.scrapeToday()
  df = clean.cleanTweets(df)
  df = extract.extractSentiment(df)
  df = extract.extractWeightedSentiment(df)

  return df.iloc[0]["weighted_sentiment"]



if __name__ == '__main__':
  app.run()