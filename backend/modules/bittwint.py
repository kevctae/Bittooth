
import twint
import pandas as pd
from datetime import datetime, timedelta
import nest_asyncio

# Solve compatibility issues with notebooks and RunTime errors.
nest_asyncio.apply()

# Function for running single/multiple search on a date interval
def scrape_twitter(search, limit, since, until=None, verified=False, output=""):
    
    # Initialize search configuration
    config = twint.Config()

    # Search keys
    config.Search = search

    # Search settings
    config.Lang = "en"
    config.Limit = limit
    config.Verified = verified
    
    # Output settings
    config.Hide_output = True
    if output != "":
        config.Store_csv = True
        config.Output = output
    config.Pandas = True
    
    # Run search
    if not until:
        until = since
        
    df = pd.DataFrame()
    
    # Get start and end dates
    start = datetime.strptime(since, '%Y-%m-%d')
    end = datetime.strptime(until, '%Y-%m-%d')
    delta = end - start
    
    # Loop each dates
    for i in range(1, delta.days + 2):
        itr = start + timedelta(days=i)
        config.Until = itr.strftime('%Y-%m-%d')
        
        twint.run.Search(config)
        
        df = pd.concat([df, twint.storage.panda.Tweets_df], ignore_index=True)
        df = df.drop_duplicates(subset='id')
    
    return df