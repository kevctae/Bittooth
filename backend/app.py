from flask import Flask, Response
from modules import scrape, clean, extract, prediction, prediction_no_sentiment
from datetime import datetime
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/get_predictions")
def get_predictions():
    df = pd.read_pickle("./data/predictions.pkl")
    res = df.head(7).to_json(orient="records")

    return Response(res, mimetype="application/json"), 200


@app.route("/update_predictions")
def update_predictions():
    df = pd.read_pickle("./data/predictions.pkl")
    pred_without_sentiment, open_bitcoin = prediction_no_sentiment.predict_to_string()
    df.loc[0, "actual_value"] = open_bitcoin

    sentiment = get_sentiment()
    pred_with_sentiment = prediction.predict_to_string(sentiment)

    new_row = pd.DataFrame(
        {
            "index": [df.shape[0]],
            "date": [datetime.now()],
            "sentiment": [sentiment],
            "pred": [pred_without_sentiment],
            "pred_sent": [pred_with_sentiment],
            "actual_value": 0,
        }
    )

    df = pd.concat([new_row, df], ignore_index=True)
    df.to_pickle("./data/predictions.pkl")
    res = df.head(7).to_json(orient="records")

    return Response(res, mimetype="application/json"), 200


def get_sentiment():
    df = scrape.scrapeToday()
    df = clean.cleanTweets(df)
    df = extract.extractSentiment(df)
    df = extract.extractWeightedSentiment(df)

    return df.iloc[0]["weighted_sentiment"]


if __name__ == "__main__":
    app.run()