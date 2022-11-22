# %% [markdown]
# High Value Customer Identification (Insiders)

import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, RobustScaler,MinMaxScaler
import pandas as pd
import numpy as np
import re, pickle, s3fs
from sklearn import metrics as m



endpoint = f"postgresql://master:abc123456@dbinsiders.cegm6m2znhnj.sa-east-1.rds.amazonaws.com/postgres"

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

query_collect = """
SELECT * FROM insiders
"""


conn.clear_compiled_cache()