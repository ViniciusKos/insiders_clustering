import pandas as pd
import numpy as np



def build_features(data):

     # Create a DataFrame df_ref containing unique customer IDs from data
     df_ref = data[['customerid']].drop_duplicates(ignore_index=True)

     # Calculate gross revenue for each customer
     purchases = data.loc[data['quantity'] >= 0, :]
     purchases['gross_revenue'] = purchases['quantity'] * purchases['unitprice']
     df_monetary = purchases[['customerid', 'gross_revenue']].groupby('customerid').sum().reset_index()
     df_ref = df_ref.merge(df_monetary, on='customerid', how='left').fillna(0)

     # Calculate gross outgoings and quantity of returns for each customer
     returns = data.loc[data['quantity'] < 0, :]
     returns['gross_returns'] = returns['quantity'] * returns['unitprice'] * -1
     df_returns = returns[['customerid', 'gross_returns']].groupby('customerid').sum().reset_index()
     df_ref = df_ref.merge(df_returns, on='customerid', how='left').fillna(0)

     # Calculate the recency of purchases for each customer
     df_recency = purchases.groupby(['customerid', 'invoicedate']).max().reset_index()
     df_recency['recencydays'] = (data['invoicedate'].max() - df_recency['invoicedate']).dt.days
     df_recency = df_recency[['customerid', 'recencydays']].copy()
     df_ref = df_ref.merge(df_recency, how='left', on='customerid')
     df_ref = df_ref.drop_duplicates(subset='customerid', keep='last')

     # Calculate the quantity of products purchased for each customer
     df_freq = purchases[['customerid', 'quantity']].drop_duplicates().groupby('customerid').sum().reset_index().rename(columns={'quantity': 'qtd_items'})
     df_ref = pd.merge(df_ref, df_freq, on='customerid', how='left').fillna(0)

     # Calculate the frequency of purchases for each customer
     df_aux = (data[['customerid', 'invoiceno', 'invoicedate']].drop_duplicates()
               .groupby('customerid')
               .agg(max_=('invoicedate', 'max'),
                    min_=('invoicedate', 'min'),
                    days_=('invoicedate', lambda x: ((x.max() - x.min()).days) + 1),
                    buy_=('invoiceno', 'count')).reset_index()
               )
     df_aux['frequency'] = df_aux[['buy_', 'days_']].apply(lambda x: x['buy_'] / x['days_'] if x['days_'] != 0 else 0, axis=1)
     df_ref = df_ref.merge(df_aux[['customerid', 'frequency']], on='customerid', how='left')

     # Calculate the basket size for each customer
     df_aux = purchases.groupby('customerid').agg(n_purchases_unique=('invoiceno', 'nunique'), n_products=('quantity', 'sum')).reset_index()
     df_ref = df_ref.merge(df_aux[['customerid', 'n_purchases_unique']].drop_duplicates(), how='left', on='customerid')


     #avg ticket
     df_ref['avg_ticket']=df_ref['gross_revenue']/(df_ref['qtd_items']-df_ref['qtd_returns'])
     df_ref['avg_ticket']=df_ref['avg_ticket'].replace([np.inf, -np.inf], 0) 


     #qtd items returns
     df_ref = df_ref.loc[:, df_ref.columns != "gross_returns"]
     returns = data.loc[data['quantity'] < 0, :]
     returns['qtd_returns'] = returns['quantity']*-1
     df_returns = returns[['customerid', 'qtd_returns']].groupby( 'customerid').sum().reset_index()
     df_ref = df_ref.merge(df_returns,on='customerid',how='left').fillna(0)
     

     return df_ref
