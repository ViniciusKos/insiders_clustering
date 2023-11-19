
def treat_na_customerid(data):
    df_missing = data[data['customerid'].isna()]
    df_not_missing = data[~data['customerid'].isna()]
    df_missing[df_missing['invoiceno'].isin(df_not_missing['invoiceno'])].shape

    # create reference
    df_backup = pd.DataFrame( df_missing['invoiceno'].drop_duplicates())
    df_backup['customerid']=np.arange(80000, 80000+len( df_backup ), 1)

    # merge original with reference datafarme
    data = data.merge(df_backup, on='invoiceno', how='left')

    #coalesce
    data['customerid'] = data['customerid_x'].combine_first( data['customerid_y'])

    #drop extra columns
    data = data.drop( columns=['customerid_x','customerid_y'], axis=1)


    return data
