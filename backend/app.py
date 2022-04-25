from bson.json_util import dumps
from flask import Flask, Response, current_app, g
from modules import scrape, clean, extract, prediction, prediction_no_sentiment
from datetime import datetime
import pandas as pd
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://kevctae:tz8ylgmchw2wxgej@cluster0.c8ra9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
CORS(app)


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(app).db

    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


@app.route("/get_predictions")
def get_predictions():
    last_7_predictions = get_last_7_predictions()
    json_data = dumps(last_7_predictions, indent=2)

    return Response(json_data, mimetype="application/json"), 200


@app.route("/update_predictions")
def update_predictions():
    pred_without_sentiment, open_bitcoin = prediction_no_sentiment.predict_to_string()
    doc_count = db.predictions.count_documents({})
    update_actual_value(doc_count - 1, open_bitcoin)

    sentiment = get_sentiment()
    pred_with_sentiment = prediction.predict_to_string(sentiment)

    add_prediction(
        doc_count,
        datetime.now(),
        sentiment,
        pred_without_sentiment,
        pred_with_sentiment,
        0,
    )

    last_7_predictions = get_last_7_predictions()
    json_data = dumps(last_7_predictions, indent=2)

    return Response(json_data, mimetype="application/json"), 200


def get_sentiment():
    df = scrape.scrapeToday()
    df = clean.cleanTweets(df)
    df = extract.extractSentiment(df)
    df = extract.extractWeightedSentiment(df)

    return df.iloc[0]["weighted_sentiment"]


# Mongo DB Functions


def add_prediction(index, date, sentiment, pred, pred_sent, actual_value):
    prediction_doc = {
        "index": index,
        "date": date,
        "sentiment": sentiment,
        "pred": pred,
        "pred_sent": pred_sent,
        "actual_value": actual_value,
    }

    return db.predictions.insert_one(prediction_doc)


def get_last_7_predictions():
    return list(db.predictions.find().sort("index", -1).limit(7))


def update_actual_value(index, actual_value):
    response = db.predictions.update_one(
        {"index": index}, {"$set": {"actual_value ": actual_value}}
    )

    return response


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.run()
