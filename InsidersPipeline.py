
import pickle
import gzip
import pandas as pd
from src.cleaning import cleaning
from src.features import build_features
from sklearn.ensemble import RandomForestRegressor



class InsidersPipeline( object ):
    def __init__( self ):
        self.home_path='P:\Python\GitHub\forecast_sales'
        self.rescaler_minmax = pickle.load(open("src/data_preparation/minmax.pkl", "rb"))
        self.rescaler_robust = pickle.load(open("src/data_preparation/robust.pkl", "rb"))
        self.embedding = pickle.load(gzip.open("src/data_preparation/embedding_rf.pkl.gz", "rb"))
        self.reducer = pickle.load(gzip.open("src/data_preparation/reducer_rf_umap.pkl.gz", "rb"))
        self.model = pickle.load(gzip.open("src/models/model_kmeans.pkl.gz", "rb"))
        
        
    def data_cleaning( self, data ): 
        
        data = cleaning.treat_na_customerid(data)
        data = cleaning.assign_correct_dtype(data)

        return data
    

    def feature_creation( self, data):

        data = build_features.build_features(data)

        return data
    
    def data_preparation( self, data ):

        mms_cols = ['recencydays','avg_ticket', 'frequency','gross_revenue', 'qtd_returns']
        data[mms_cols] = self.rescaler_minmax.transform(data[mms_cols])


        robust_cols = ['qtd_items', "n_purchases_unique"]
        data[robust_cols] = self.rescaler_robust.transform(data[robust_cols])

        data = self.embedding.apply(data[['qtd_returns', 'recencydays', 'qtd_items', 'avg_ticket', 'frequency',
       'n_purchases_unique']])
        data = pd.DataFrame(data)

        data = self.reducer.transform(data)
        data = pd.DataFrame({"umap_embedding_x": data[:,0],
                         "umap_embedding_y":data[:,1]})

        return data


    def predict(self, data ):

        clusters = self.model.predict(data)
        
        
        return clusters
        

        
