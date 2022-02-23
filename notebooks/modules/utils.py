# basic data-handling dataframes
import pandas as pd
import numpy as np

# libraries used in dataimports and modifications
from tvDatafeed import TvDatafeed, Interval
import pandas_ta as ta
import requests
import json
import datetime

# libraries used to clean twitter data
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
english_stop_words = stopwords.words('english')


### Methods to clean twitter data

def repl(matchObj):
    '''
    
    ''''
    char = matchObj.group(1)
    return "%s%s" % (char, char)


def clean_tweet(tweet):
    '''
    Function to preprocess twitter sentences
    Arguments:
    tweet - tweet (string)
    
    Output - cleaned tweet (string)'''
    
    tweet = tweet.lower()
    # remove URL "https://t.co/"
    new_url = re.sub(r"https://t.co/[A-Za-z0-9]+", " ", tweet)
    
    # remove mention
    tweet = re.sub(r"@[A-Za-z0-9!#%&*;_\$\.]+", " ", new_url)
    
    # remove # ,turning hashtags to the typical words.
    tweet = re.sub(r"\W+", " ", tweet)
    
    # reduce character sequences >3 to 3
    tweet = re.sub(re.compile(r"(\w)\1+"), repl, tweet)

    # remove 2-character words
    tweet = re.sub(r"\b[a-z]{1,2}\b", " ", tweet)
    
    # replace 2 or more spaces with a single space.
    tweet = re.sub(r"\s+", " ", tweet)
    
    # remove spaces front and back
    tweet = re.sub(r"^\s+|\s$", "", tweet)
    
    # remove stop words
    tweet = ' '.join([word for word in tweet.split() 
                      if word not in english_stop_words])
    
    return cleaned_tweet


def remove_stop_words(tweet):
    ''' 
    '''
    
    tweet_removed = ' '.join([word for word in tweet.split() 
                      if word not in english_stop_words])
    
    return tweet_removed


def processed_twitter_data(link = '../data/interim/tweets_verified_2020-2021.pkl'):
    '''Function to return preprcessed twitter data
    Arguments:
    link - link to the pkl data
    
    Output:
    df - dataframe of cleaned twitter'''
    
    # first download twitter data
    df = pd.read_pickle(link)
    
    # apply first cleaning on the tweets
    # language EN only
    df = df[df['language'] == 'en']

    # apply cleaninging 1
    df['tweet'] = df['tweet'].progress_apply(clean_tweet_1)
    
    
    
    return df








### methods for importing bitcoin price data
def get_data(symbol_name, exchange = 'BINANCE',start_date = "2020-01-01"):
    
    # instanciate the library and get historiacal data
    tv = TvDatafeed()
    data=tv.get_hist(symbol=symbol_name,exchange=exchange,interval=Interval.in_daily,n_bars=5000)
    data=data.reset_index()
    
    # reformat and subset the data
    data["datetime"]=data["datetime"].dt.strftime('%Y-%m-%d')
    data2=data[data["datetime"]>=start_date].copy()
    data2["datetime"] = pd.to_datetime(data2["datetime"])
    
    return data2


def getapi(api, start_date = "2020-01-01"):
    
    response_API=requests.get(api)
    data=response_API.text
    parse_json=json.loads(data)
    df = pd.json_normalize(parse_json['values'])
    listtime=list(df['x'])
    listtime2=[]
    for i in listtime:
        listtime2.append(datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d'))
    df['datetime']=pd.Series(listtime2)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df=df[df["datetime"] >= start_date].copy()
    df=df.drop(columns=['x'])
    df.rename(columns={'y':'value'},inplace=True)
    df=df.drop_duplicates(subset=['datetime'])
    
    return df

def calculate_return(df, columns, n):
    '''
    function to calculate returns
    Arguments:
    df - dataframe we use
    column - column for which we calculate returns (str or list of strings)
    n - time window for which we calculate return
    Output:
    df - dataframe with new columns containig return data'''

    if type(columns) == list:
        for column in columns:
            df[column+'_return'] = df[column].pct_change(n)

    elif type(columns)==str:
        df[columns+'_return'] = df[columns].pct_change(n)

    return df



def lag_columns(df, columns, n):
    '''
    function to lagg certain columns by a specific number of rows
    Arguments:
    df - dataframe to use
    columns - columns for which we lag the data
    n - number of rows we lag the data (positive or negative)
    Output:
    df - dataframe with new columns containing lagged data
    '''
    
    if type(columns) == list:
        for column in columns:
            df[column+"_"+str(n)+"_days_lagged"] = df[column].shift(periods = n)
    elif type(columns)==str:
        df[columns+"_"+str(n)+"_days_lagged"] = df[columns].shift(periods = n)
        
    return df

