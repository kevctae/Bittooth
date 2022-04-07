import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# sp = spacy.load('en_core_web_sm')

def extractSentiment(df):
  sent_obj = SentimentIntensityAnalyzer()
  sent_data = df['tweet']

  pest_words = {
      'up': 2.0,
      'down': -2.0,
      'green' : 2.0,
      'red' : -2.0,
      'bull' : 2.0,
      'bear' : -2.0,
      'buy' : 2.0,
      'bought' : 2.0,
      'sell' : -2.0,
      'sold' : -2.0,
      'moon': 2
  }

  new_si = SentimentIntensityAnalyzer()
  new_si.lexicon.update(pest_words)

  sentiment_update = []
  for i in sent_data:
    sentiment_update.append(sent_obj.polarity_scores(i))
  
  all_compound = [one_tok['compound'] for one_tok in sentiment_update]
  df['sentiment'] = pd.DataFrame(all_compound)

  return df

def extractWeightedSentiment(df):
  df['sum_metrics'] = df['nreplies'] + \
                      df['nretweets'] + \
                      df['nlikes']

  weights = pd.read_pickle("./models/weights.pkl")

  df = pd.merge(df,\
              weights[['sum_metrics', 'weights']], \
              how='left', \
              on='sum_metrics')

  df['weighted_sentiment'] = df['sentiment'] * df['weights']

  df_by_date = df.groupby(df['created_at'].dt.date).agg({'weighted_sentiment': 'mean'}).reset_index()
  df_by_date["created_at"] = pd.to_datetime(df_by_date["created_at"])
  df_by_date = df_by_date.rename(columns={'created_at': 'datetime'})

  return df_by_date