import nest_asyncio
nest_asyncio.apply()

import twint
import pandas as pd
from datetime import datetime, timedelta
from tqdm.notebook import tqdm

# Function for running single/multiple search on a date interval
def scrape_twitter(search, limit, since, until=None, output="../data/output.csv"):
    
    # Initialize search configuration
    config = twint.Config()

    # Search keys
    config.Search = search

    # Search settings
    config.Lang = "en"
    config.Limit = limit
    config.Verified = False
    
    # Output settings
    config.Hide_output = True
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
    for i in tqdm(range(1, delta.days + 2)):
        itr = start + timedelta(days=i)
        config.Until = itr.strftime('%Y-%m-%d')
        
        twint.run.Search(config)
        
        df = pd.concat([df, twint.storage.panda.Tweets_df], ignore_index=True)
        df = df.drop_duplicates(subset='id')
    
    return df