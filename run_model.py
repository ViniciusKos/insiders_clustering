# %% [run_model]
# High Value Customer Identification (Insiders)

# %%
import sqlite3
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, RobustScaler,MinMaxScaler
import pandas as pd
import seaborn as sns
import numpy as np
import re
import matplotlib.pyplot as plt
from sklearn import cluster as c 
from sklearn import metrics as m
from yellowbrick.cluster import KElbowVisualizer, SilhouetteVisualizer
import matplotlib.gridspec as gridspec
from plotly import express as px
import pylab 
import scipy.stats as stats
import statsmodels.api as sm
from sklearn.mixture import GaussianMixture
from scipy.cluster import hierarchy as hc 
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import KBinsDiscretizer
from getpass import getpass
import os
import pickle
import s3fs


plt.rcParams["figure.figsize"] = (15,8)


# %%
aws_key_id = os.environ.get( "AWS_ACCESS_KEY_ID" )
aws_key_secret = os.environ.get( "AWS_SECRET_ACCESS_KEY" )

# %% [markdown]
# ## 0.2 Load dataset

# %%
df0 = pd.read_csv('s3://insiders-clustering-deploy/data.csv', storage_options={ "key":aws_key_id,
                                                                                "secret":aws_key_secret}, encoding='latin1')
df0.columns=df0.columns.str.lower()
df0.head(3)

# %%
df1=df0.copy()

# %%
df_missing=df1[df1['customerid'].isna()]
df_not_missing=df1[~df1['customerid'].isna()]
df_missing[df_missing['invoiceno'].isin(df_not_missing['invoiceno'])].shape

# %%
# create reference
df_backup = pd.DataFrame( df_missing['invoiceno'].drop_duplicates())
df_backup['customerid']=np.arange(80000, 80000+len( df_backup ), 1)

# merge original with reference datafarme
df1 = df1.merge(df_backup, on='invoiceno', how='left')

#coalesce
df1['customerid']=df1['customerid_x'].combine_first( df1['customerid_y'])

#drop extra columns
df1 = df1.drop( columns=['customerid_x','customerid_y'], axis=1)

df1.isna().sum()

# %% [markdown]
# ## 1.3 data types treatment

# %%
df1['invoicedate']=df1['invoicedate'].str.split(expand=True)[0]
df1.head()

# %%
df1['invoicedate'] = pd.to_datetime( df1['invoicedate'], format="%m/%d/%Y",errors='coerce')
df1['customerid'] = df1['customerid'].astype(int)

# %% [markdown]
# # 2.0 Feature Filtering/Cleaning

# %%
df2=df1.copy()

# %%
 # ----------------------  Numerical attributes ----------------
 # purhcases df and returns df
returns = df2.loc[df2['quantity'] < 0, :]
purchases = df2.loc[df2['quantity'] >= 0, :]


print(df2.shape)


#drop invoices with only letters
df2=df2[~df2['invoiceno'].str.contains('[^0-9]+', na=False)]
print(df2.shape)

#filter only stockcodes with numbers
#df2=df2[df2['stockcode'].str.contains('[0-9]+', na=False)]
print(df2.shape)


# ------------------ Categorical attributes -------------------
# drop description
df2 = df2.drop( columns='description', axis=1 )

# drop "unspecifiec" and "european communoty" countries -  
df2 = df2[~df2['country'].isin( ["European Community",'Unspecified' ] ) ]


# --------------------- Filter bad customer ----------------- (Section 5 Exploratory Data Analysis)
df2=df2[df2['customerid']!=16446]

# %%
df_ref=df2[['customerid']].drop_duplicates(ignore_index=True)

# %% [markdown]
# ### 3.1.1 profit (gross revenue - gross outgoings)

# %%
# gross revenue
purchases['gross_revenue'] = purchases['quantity'] * purchases['unitprice']
df_monetary = purchases[['customerid', 'gross_revenue']].groupby( 'customerid').sum().reset_index()
df_ref=df_ref.merge(df_monetary,on='customerid',how='left').fillna(0)


# gross outgoings
returns['gross_returns'] = returns['quantity'] * returns['unitprice']*-1
df_returns = returns[['customerid', 'gross_returns']].groupby( 'customerid').sum().reset_index()
df_ref=df_ref.merge(df_returns,on='customerid',how='left').fillna(0)

# %% [markdown]
# ### 3.1.2 recency

# %%
#recency
df_recency = purchases.groupby( 'customerid').max().reset_index()
df_recency['recencydays'] = ( purchases['invoicedate'].max() - df_recency['invoicedate'] ).dt.days
df_recency= df_recency[['customerid','recencydays']].copy()
df_ref=df_ref.merge(df_recency, how='left', on='customerid')

# %% [markdown]
# ### 3.1.3 quantity of items kept

# %%
# quantity of products purchased
df_freq = purchases[['customerid', 'quantity']].drop_duplicates().groupby( 'customerid' ).sum().reset_index().rename( columns={'quantity':'qtd_items'})
df_ref = pd.merge( df_ref, df_freq, on='customerid', how='left' ).fillna(0)

# %%
df_freq = returns[['customerid', 'quantity']].drop_duplicates().groupby( 'customerid' ).sum().reset_index().rename( columns={'quantity':'qtd_items_return'})
df_freq['qtd_items_return'] = df_freq['qtd_items_return']*-1
df_ref = pd.merge( df_ref, df_freq, on='customerid', how='left' ).fillna(0)

# %% [markdown]
# ### 3.1.4 avg ticket

# %%
df_ref['avg_ticket']=df_ref['gross_revenue']/(df_ref['qtd_items']-df_ref['qtd_items_return'])
df_ref['avg_ticket']=df_ref['avg_ticket'].replace([np.inf, -np.inf], 0) 
df_ref.isna().sum()

# %% [markdown]
# ### 3.1.5 frequency

# %%
# frequency

df_aux = ( df2[['customerid', 'invoiceno', 'invoicedate']].drop_duplicates()
                                                        .groupby('customerid')
                                                        .agg( max_ = ('invoicedate', 'max'),
                                                            min_= ('invoicedate', 'min'),
                                                            days_= ('invoicedate', lambda x: (( x.max() - x.min()).days ) +1 ),
                                                            buy_ = ('invoiceno', 'count')).reset_index()
)

df_aux['frequency'] = df_aux[['buy_', 'days_']].apply(lambda x: x['buy_']/x['days_'] if x['days_'] != 0 else 0, axis=1)

df_ref= df_ref.merge(df_aux[['customerid','frequency']], on='customerid', how='left')

df_ref.isna().sum()

# %% [markdown]
# ### 3.1.6 basket size

# %%
df_aux = ( purchases.loc[:, ['customerid', 'invoiceno', 'quantity']].groupby( 'customerid' )
                                                                            .agg( n_purchase=( 'invoiceno', 'nunique'),
                                                                                  n_products=( 'quantity', 'sum' ) )
                                                                            .reset_index() )

# calculation
df_aux['avg_basket_size'] = df_aux['n_products'] / df_aux['n_purchase']

# merge
df_ref = pd.merge( df_ref, df_aux[['customerid', 'avg_basket_size']], how='left', on='customerid' )
df_ref.isna().sum()

# %% [markdown]
# ### 3.1.7 nunique items

# %%
# basket size
df_aux = ( purchases.groupby('customerid').agg( n_purchases_unique = ('invoiceno','nunique'), n_products = ('quantity','sum'))
                                            .reset_index()
)
#calculation
df_ref = df_ref.merge( df_aux[['customerid', 'n_purchases_unique']], how='left', on='customerid')
print(df_ref.isna().sum())

df_ref.head()

# %% [markdown]
# ## 4.2 Filters Applied

# %%
df5=df_ref.copy()

# %%
print(df5.shape)
df5=df5[df5['customerid']!=16446]
df5=df5[df5['customerid']!=14646]
df5=df5[df5['avg_ticket']>0]
df5['avg_ticket']=df5['avg_ticket'].fillna(0)
print(df5.shape)

# %%
fs = s3fs.S3FileSystem( anon=False, key=aws_key_id, secret= aws_key_secret)

mms_cols=[ 'recencydays',
        'avg_ticket', 'frequency',
       'avg_basket_size', 'n_purchases_unique']

rs_cols=['gross_revenue', 'gross_returns', 
       'qtd_items', 'qtd_items_return',]
       

for i in mms_cols:
     mms=pd.read_pickle(f"s3://insiders-clustering-deploy/artifacts/{i}_minmax.pkl")
     df5[[i]] = mms.transform(df5[[i]])

for i in rs_cols:
     kb=pd.read_pickle(f"s3://insiders-clustering-deploy/artifacts/{i}_kbins.pkl")
     df5[[i]] = kb.transform(df5[[i]])

# %% [markdown]
# # 8.0  Model Training

# %%
X=df5.drop(columns=['customerid'])

# %%
X.head()

# %%
km = pd.read_pickle(f"s3://insiders-clustering-deploy/artifacts/model.pkl")

vis_silhouette = SilhouetteVisualizer(km, colors='yellowbrick')
vis_silhouette.fit(X)
vis_silhouette.finalize()

# %%
df8=df5.copy()
df8['cluster']=km.labels_
df8.groupby('cluster').mean().style.highlight_max( color='green', axis=0)

# %%
df8['cluster'].value_counts(normalize=True).sort_index()
## The Insiders (cluster 1) cluster has a lot of customers, considering a real world situation, it is not good to the marketing team afford so many customers.

# %%
df8['cluster'].value_counts().sort_index()

# %% [markdown]
# # 9.0 Deploy to production

# %%
df9=df8.copy()
df9.head(3)

# %%
for i in ['recencydays','qtd_items','qtd_items_return']:
    df9[i]=df9[i].astype(int)

# %%

endpoint = "database-1.cegm6m2znhnj.sa-east-1.rds.amazonaws.com"

 #create table
query_create_table_insiders = """
    CREATE TABLE IF NOT EXISTS insiders ( 
       grossrevenue   REAL,
       gross_returns    REAL,
       recencydays    REAL,   
       qtd_items   REAL,
       qtd_items_return     REAL,
       avg_ticket   REAL,
       frequency       REAL,
       avg_basket_size  REAL,
       n_purchases_unique   REAL,
       cluster         INTEGER
   )
"""


conn = sqlite3.connect( 'insiders_db.sqlite' )
conn.execute( query_create_table_insiders )
conn.commit()
conn.close()

# insert data
conn = create_engine( 'sqlite:///insiders_db.sqlite' )
df9.to_sql( 'insiders', con=conn, if_exists='append', index=False )

# %%
pass_database=getpass()

# %%
endpoint = f"postgresql://postgres:{pass_database}@database-2.cegm6m2znhnj.sa-east-1.rds.amazonaws.com/postgres"


conn = create_engine( endpoint)



 #create table
query_create_table_insiders = """
    CREATE TABLE IF NOT EXISTS insiders ( 
       grossrevenue   REAL,
       gross_returns    REAL,
       recencydays    REAL,   
       qtd_items   REAL,
       qtd_items_return     REAL,
       avg_ticket   REAL,
       frequency       REAL,
       avg_basket_size  REAL,
       n_purchases_unique   REAL,
       cluster         INTEGER
   )
"""


# conn = sqlite3.connect( 'insiders_db.sqlite' )
# conn.execute( query_create_table_insiders )
# conn.commit()
# conn.close()

# insert data
df9.to_sql( 'insiders', con=conn, if_exists='replace', index=False )



# %%
conn.close()

# %%
#get query

query_collect = """
SELECT * FROM insiders
"""

df=pd.read_sql_query( query_collect, conn)
df.head()

# %%



