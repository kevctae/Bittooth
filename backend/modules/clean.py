import nltk
from nltk.corpus import stopwords
import re
import pandas as pd

nltk.download('stopwords')
english_stop_words = stopwords.words('english')

def cleanTweets(df):
  english_stop_words = stopwords.words('english')
  add_stopwords = ['bitcoin', 'btc', 'crypto', 'cryptocurrency', 'cryptocurrencies',
                  'ethereum', 'eth', 'price', 'prices', 'money', 'dollars']
  remove_stopwords = ['up','down']
  english_stop_words = english_stop_words + add_stopwords

  for i in remove_stopwords:
      if i in english_stop_words:
          english_stop_words.remove(i)

  df = df[df['language'] == 'en']
  df['tweet_clean'] = pd.DataFrame(df['tweet'].str.lower())

  df['tweet_clean'] = df['tweet_clean'].apply(clean_tweet_1)
  df = df.drop_duplicates(subset='tweet_clean', keep=False)
  df['tweet_clean'] = remove_stop_words(df['tweet_clean'])
  df['tweet_clean'] = df['tweet_clean'].apply(clean_tweet_2)

  return df

def repl(matchObj):
    char = matchObj.group(1)
    return "%s%s" % (char, char)

def remove_stop_words(corpus):
    removed_stop_words = []
    for review in corpus:
        removed_stop_words.append(
            ' '.join([word for word in review.split() 
                      if word not in english_stop_words])
        )
    return removed_stop_words

def clean_tweet_1(tweet):
    # remove URL "https://t.co/"
    new_url = re.sub(r"https://t.co/[A-Za-z0-9]+", " ", tweet)
    
    # remove mention
    new_mention = re.sub(r"@[A-Za-z0-9!#%&*;_\$\.]+", " ", new_url)
    
    # remove # ,turning hashtags to the typical words.
    new_symbol = re.sub(r"\W+", " ", new_mention)
    
    # remove number
    new_number = re.sub(r"[0-9]", "", new_symbol)
    
    return new_number

def clean_tweet_2(tweet):
    # reduce character sequences >3 to 3
    new_sequence = re.sub(re.compile(r"(\w)\1+"), repl, tweet)
    
    # replace 2 or more spaces with a single space.
    new_space = re.sub(r"\s+", " ", new_sequence)
    
    # remove spaces front and back
    new_space_end = re.sub(r"^\s+|\s$", "", new_space)
    
    return new_space_end