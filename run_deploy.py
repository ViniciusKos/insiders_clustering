# %% [markdown]
# High Value Customer Identification (Insiders)

import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, RobustScaler,MinMaxScaler
import pandas as pd
import numpy as np
import re, pickle, s3fs
from sklearn import metrics as m




#df0 = pd.read_parquet('data.parquet') 

fs = s3fs.S3FileSystem(anon=False)

df0 = pd.read_parquet("s3://insiders-clustering-deploy/data.parquet")
df0.columns=df0.columns.str.lower()
df0.head(3)


df1=df0.copy()

df_missing=df1[df1['customerid'].isna()]
df_not_missing=df1[~df1['customerid'].isna()]
df_missing[df_missing['invoiceno'].isin(df_not_missing['invoiceno'])].shape

df_backup = pd.DataFrame( df_missing['invoiceno'].drop_duplicates())
df_backup['customerid']=np.arange(80000, 80000+len( df_backup ), 1)

df1 = df1.merge(df_backup, on='invoiceno', how='left')
df1['customerid']=df1['customerid_x'].combine_first( df1['customerid_y'])
df1 = df1.drop( columns=['customerid_x','customerid_y'], axis=1)
df1['invoicedate']=df1['invoicedate'].str.split(expand=True)[0]
df1['invoicedate'] = pd.to_datetime( df1['invoicedate'], format="%m/%d/%Y",errors='coerce')
df1['customerid'] = df1['customerid'].astype(int)



df2=df1.copy()
returns = df2.loc[df2['quantity'] < 0, :]
purchases = df2.loc[df2['quantity'] >= 0, :]
df2=df2[~df2['invoiceno'].str.contains('[^0-9]+', na=False)]


df2 = df2.drop( columns='description', axis=1 )
df2 = df2[~df2['country'].isin( ["European Community",'Unspecified' ] ) ]
df2=df2[df2['customerid']!=16446]

df_ref=df2[['customerid']].drop_duplicates(ignore_index=True)

purchases['gross_revenue'] = purchases['quantity'] * purchases['unitprice']
df_monetary = purchases[['customerid', 'gross_revenue']].groupby( 'customerid').sum().reset_index()
df_ref=df_ref.merge(df_monetary,on='customerid',how='left').fillna(0)


returns['gross_returns'] = returns['quantity'] * returns['unitprice']*-1
df_returns = returns[['customerid', 'gross_returns']].groupby( 'customerid').sum().reset_index()
df_ref=df_ref.merge(df_returns,on='customerid',how='left').fillna(0)

df_recency = purchases.groupby( 'customerid').max().reset_index()
df_recency['recencydays'] = ( purchases['invoicedate'].max() - df_recency['invoicedate'] ).dt.days
df_recency= df_recency[['customerid','recencydays']].copy()
df_ref=df_ref.merge(df_recency, how='left', on='customerid')

df_freq = purchases[['customerid', 'quantity']].drop_duplicates().groupby( 'customerid' ).sum().reset_index().rename( columns={'quantity':'qtd_items'})
df_ref = pd.merge( df_ref, df_freq, on='customerid', how='left' ).fillna(0)

df_freq = returns[['customerid', 'quantity']].drop_duplicates().groupby( 'customerid' ).sum().reset_index().rename( columns={'quantity':'qtd_items_return'})
df_freq['qtd_items_return'] = df_freq['qtd_items_return']*-1
df_ref = pd.merge( df_ref, df_freq, on='customerid', how='left' ).fillna(0)

df_ref['avg_ticket']=df_ref['gross_revenue']/(df_ref['qtd_items']-df_ref['qtd_items_return'])
df_ref['avg_ticket']=df_ref['avg_ticket'].replace([np.inf, -np.inf], 0) 
df_ref.isna().sum()

df_aux = ( df2[['customerid', 'invoiceno', 'invoicedate']].drop_duplicates()
                                                        .groupby('customerid')
                                                        .agg( max_ = ('invoicedate', 'max'),
                                                            min_= ('invoicedate', 'min'),
                                                            days_= ('invoicedate', lambda x: (( x.max() - x.min()).days ) +1 ),
                                                            buy_ = ('invoiceno', 'count')).reset_index()
)

df_aux['frequency'] = df_aux[['buy_', 'days_']].apply(lambda x: x['buy_']/x['days_'] if x['days_'] != 0 else 0, axis=1)
df_ref= df_ref.merge(df_aux[['customerid','frequency']], on='customerid', how='left')

df_aux = ( purchases.loc[:, ['customerid', 'invoiceno', 'quantity']].groupby( 'customerid' )
                                                                            .agg( n_purchase=( 'invoiceno', 'nunique'),
                                                                                  n_products=( 'quantity', 'sum' ) )
                                                                            .reset_index() )

df_aux['avg_basket_size'] = df_aux['n_products'] / df_aux['n_purchase']
df_ref = pd.merge( df_ref, df_aux[['customerid', 'avg_basket_size']], how='left', on='customerid' )
df_aux = ( purchases.groupby('customerid').agg( n_purchases_unique = ('invoiceno','nunique'), n_products = ('quantity','sum'))
                                            .reset_index()
)


df_ref = df_ref.merge( df_aux[['customerid', 'n_purchases_unique']], how='left', on='customerid')

df_ref.head()

df5=df_ref.copy()

df5=df5[df5['customerid']!=16446]
df5=df5[df5['customerid']!=14646]
df5=df5[df5['avg_ticket']>0]
df5['avg_ticket']=df5['avg_ticket'].fillna(0)
print(df5.shape)


mms_cols=['recencydays','avg_ticket', 'frequency','avg_basket_size', 'n_purchases_unique','gross_revenue', 'gross_returns', 'qtd_items', 'qtd_items_return',]


       
for i in mms_cols:
     mms=pd.read_pickle(f"s3://insiders-clustering-deploy/artifacts/{i}_minmax.pkl")
     df5[[i]] = mms.transform(df5[[i]])


X=df5.drop(columns=['customerid'])


# %%
#km = pd.read_pickle(f"s3://insiders-clustering-deploy/artifacts/model.pkl")

reducer = pd.read_pickle(f"s3://insiders-clustering-deploy/artifacts/umap_reducer.pkl")
km = pd.read_pickle(f"s3://insiders-clustering-deploy/artifacts/model.pkl")

# %%
df8=df5.copy()


df8 = pd.DataFrame(reducer.transform(df8.drop('customerid', axis=1)) , columns=['embedding_x', 'embedding_y'])
df8['cluster']=km.predict(df8)



df9=df5.copy()
df9['cluster']=df8['cluster']

for i in ['recencydays','qtd_items','qtd_items_return']:
    df9[i]=df9[i].astype(int)


endpoint = f"postgresql://master:vinny123@dbinsiders.cegm6m2znhnj.sa-east-1.rds.amazonaws.com/postgresql"

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


conn.execute( query_create_table_insiders )

df9.to_sql( 'insiders', con=conn, if_exists='replace', index=False )
query_collect = """
SELECT * FROM insiders
"""

df=pd.read_sql_query( query_collect, conn)

print("df collected", df.head())

conn.clear_compiled_cache()

print(df9.head())
print('rodou tudo')
print( m.silhouette_score(df8.drop('cluster', axis=1), df8['cluster']))




