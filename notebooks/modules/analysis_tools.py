






def calculate_return(df, columns, n):
 '''
function to calculate returns

Arguments:
df - dataframe we use
column - column for which we calculate returns (str or list of strings)
n - '''   
    if type(columns) == list:
        for column in columns:
            df[column+'_return'] = df[column].pct_change(n)
            
    elif type(columns)==str:
        df[columns+'_return'] = df[columns].pct_change(n)
    
    return df


