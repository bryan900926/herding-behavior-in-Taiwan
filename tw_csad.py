import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.lines import Line2D
import os


df = pd.read_csv(r"C:\Users\bryan\OneDrive\桌面\python\data_for_qa\tw&us.csv")
df['market_return^2'] = df['market_return']**2
df['abs_market_return'] = abs(df['market_return'])
df['usreturn_lag_one'] = df['usreturn_lag_one']*100
df['us_return_lag_one^2'] = df['usreturn_lag_one']**2
industries = ['Miscellaneous', 'Paper and Packaging', 'Tourism and Leisure', 'Uncategorized'
              , 'Technology and Electronics', 'Consumer Goods and Services', 'Finance and Insurance'
              , 'Energy and Environment', 'Manufacturing and Materials', 
              'Cultural and Creative Industries', 'whole_market', 'Agriculture and Biotechnology']
def rolling_ols(window_size,variale):
   filter_df = df[['CSAD','abs_market_return','market_return^2','us_return_lag_one^2','date']]
   filter_df=filter_df.dropna()
   new_data = pd.DataFrame(columns=['date','t-value'])
   for i in range(0,len(filter_df) - window_size + 1):
      df_rolling = filter_df[i:i+window_size]
      X = sm.add_constant(df_rolling[['abs_market_return','market_return^2','us_return_lag_one^2']])
      Y = df_rolling['CSAD']
      ols_model = sm.OLS(Y, X).fit()
      new_row = pd.DataFrame({'date': [df_rolling.iloc[-1]['date']], 't-value': [ols_model.tvalues['us_return_lag_one^2']]})
      new_data = pd.concat([new_data,new_row],ignore_index=True)
   filename = rf"C:\Users\bryan\OneDrive\桌面\python\{variale}.csv"
   if os.path.isfile(filename):
       new_data.to_csv(filename, mode='a', header=False, index=False)
   else:
       new_data.to_csv(filename, mode='w', header=True, index=False)

rolling_ols(250,'tw_us_market')
