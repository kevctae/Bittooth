from . import bittwint
import pandas as pd
import datetime as dt

def scrapeToday():
  df = bittwint.scrape_twitter(
    "bitcoin", 
    1000, 
    dt.datetime.today().strftime('%Y-%m-%d'), 
    verified=True,
  )

  df = df.drop_duplicates(subset=['id'])

  df = df.drop(columns=['date', 'timezone', \
                      'place', 'retweet', 'near', 'geo', 'source', \
                      'user_rt_id', 'user_rt', 'retweet_id', 'retweet_date', \
                      'translate', 'trans_src', 'trans_dest'])

  df["created_at"] = pd.to_datetime(df["created_at"], format='%Y-%m-%d')

  df = df.astype({
      'username': 'string',
      'name': 'string',
      'tweet': 'string',
      'language': 'string',
      'link': 'string',
      'quote_url': 'string',
      'video': 'bool',
      'thumbnail': 'string',
  })

  return df
