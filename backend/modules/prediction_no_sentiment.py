import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import Ridge
import datetime
import requests
import json
import joblib
from tvDatafeed import TvDatafeed, Interval

def getdata(name):
  tv = TvDatafeed()
  data=tv.get_hist(symbol=name,exchange='BINANCE',interval=Interval.in_daily,n_bars=10)
  data=data.reset_index()
  data["datetime"]=data["datetime"].dt.strftime('%Y-%m-%d')
  data["datetime"] = pd.to_datetime(data["datetime"])
  return data

def getapi(api):
  response_API=requests.get(api)
  data=response_API.text
  parse_json=json.loads(data)
  df = pd.json_normalize(parse_json['values'])
  print(df.columns)
  listtime=list(df['x'])
  listtime2=[]
  for i in listtime:
    listtime2.append(datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d'))
  df['datetime']=pd.Series(listtime2)
  df["datetime"] = pd.to_datetime(df["datetime"])
  df=df.drop(columns=['x'])
  df.rename(columns={'y':'value'},inplace=True)
  df=df.drop_duplicates(subset=['datetime'])
  return df

def predict_to_string():
  bitcoin=getdata('BTCUSDT')
  eth=getdata('ETHUSDT')
  ada=getdata('ADAUSDT')

  number_transactions=getapi('https://api.blockchain.info/charts/n-transactions?timespan=10days&rollingAverage=24hours&format=json&sampled=false')
  number_address=getapi('https://api.blockchain.info/charts/n-unique-addresses?timespan=10days&rollingAverage=24hours&format=json&sampled=false')
  transaction_second=getapi('https://api.blockchain.info/charts/transactions-per-second?timespan=10days&rollingAverage=24hours&format=json&sampled=false')
  transaction_second=transaction_second.groupby(['datetime']).mean().reset_index()
  total_bitcoin=getapi('https://api.blockchain.info/charts/total-bitcoins?timespan=1months&rollingAverage=24hours&format=json&sampled=true')
  hash_rate=getapi('https://api.blockchain.info/charts/hash-rate?timespan=10days&rollingAverage=24hours&format=json&sampled=false')

  bitcoin=bitcoin[["datetime","open","close"]]

  bitcoin=bitcoin.merge(eth[["datetime","open"]],on='datetime',how='left',suffixes=('_bitcoin', '_eth'))
  bitcoin=bitcoin.merge(ada[["datetime","open"]],on='datetime',how='left')

  data_api=number_transactions.merge(number_address,on='datetime',how='left',suffixes=('_number_transaction', '_number_address'))
  data_api=data_api.merge(transaction_second,on='datetime',how='left')
  data_api=data_api.merge(total_bitcoin,on='datetime',how='left',suffixes=('_transaction_second', '_total_bitcoin'))
  data_api=data_api.merge(hash_rate,on='datetime',how='left')
  data_api.rename(columns={'value':'value_hash_rate'},inplace=True)

  bitcoin=bitcoin.merge(data_api,on='datetime',how='left')
  bitcoin.rename(columns={'open':'open_ada'},inplace=True)
  bitcoin.rename(columns={'close':'close_bitcoin'},inplace=True)

  temp=bitcoin["datetime"]
  bitcoin=bitcoin.drop(columns=['datetime'])
  bitcoin=bitcoin.interpolate()
  bitcoin['datetime']=temp

  selected_features=['open_bitcoin', 'open_eth', 'open_ada', 'value_number_transaction',
    'value_number_address', 'value_transaction_second',
    'value_total_bitcoin', 'value_hash_rate']
  today=bitcoin[selected_features][-1:]

  model_from_joblib = joblib.load('./modules/savedmodel_no_sentiment.pkl')
  scaler_from_joblib = joblib.load('./modules/savedscaler_no_sentiment.pkl')
  today_transformed = scaler_from_joblib.transform(today).copy()
  prediction = model_from_joblib.predict(today_transformed)

  return prediction[0][0]
