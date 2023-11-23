
import pandas as pd
import numpy as np

def treat_na_customerid(data):
    df_missing = data[data['customerid'].isna()]
    df_not_missing = data[~data['customerid'].isna()]
    df_missing[df_missing['invoiceno'].isin(df_not_missing['invoiceno'])].shape

    # create reference
    df_backup = pd.DataFrame( df_missing['invoiceno'].drop_duplicates())
    df_backup['customerid']=np.arange(80000, 80000+len( df_backup ), 1)

    # merge original with reference datafarme
    data = data.merge(df_backup, on='invoiceno', how='left')
    print(data.shape)

    #coalesce
    data['customerid'] = data['customerid_x'].combine_first( data['customerid_y'])

    #drop extra columns
    data = data.drop( columns=['customerid_x','customerid_y'], axis=1)
    return data


def assign_correct_dtype(data):

    print(data.shape)
    data['invoicedate'] = data['invoicedate'].str.split(expand=True)[0]
    data['invoicedate'] = pd.to_datetime( data['invoicedate'], format="%m/%d/%Y",errors='coerce')
    data['customerid'] = data['customerid'].astype(int)
    data = data[~data['invoiceno'].str.contains('[^0-9]+', na=False)]
    data = data.drop( columns='description', axis=1 )
    print(data.shape)
    return data



