import json
import pickle
import numpy as np
import pandas as pd
from flask import Flask,request,app,jsonify,url_for,render_template



app = Flask(__name__)

# Load the model


from src.cleaning.cleaning import treat_na_customerid


cleaning = pickle.load(open("src/models/KMeans.pkl", "rb"))
rescaler_minmax = pickle.load(open("src/rescalers/minmax.pkl", "rb"))
rescaler_robust = pickle.load(open("src/rescalers/robust.pkl", "rb"))
embedding = pickle.load(open("src/embedding/embedding_rf.pkl", "rb"))
reducer = pickle.load(open("src/reducers/reducer_rf_umap.pkl", "rb"))
model = pickle.load(open("src/models/KMeans.pkl", "rb"))
df = pd.read_parquet("data/raw/data.parquet")



@app.route("/")
def home():
    return render_template("home.html")

@app.route('/predict_api', methods = ["POST"])

def predict_api():
    data = request.json["data"]
    print(data)
    print(np.array(np.list(data.values())).reshape(1, -1))
    new_data = scalar.transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(new_data)
    print(output[0])
    return jsonify(output[0])

if __name__ == "__main__":
    app.run(debug = True)