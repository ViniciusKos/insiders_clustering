import json
import pickle
import numpy as np
import pandas as pd
from flask import Flask,request,app,jsonify,url_for,render_template



app = Flask(__name__)

from InsidersPipeline import InsidersPipeline
pipe = InsidersPipeline()



@app.route("/")
def home():
    return render_template("home.html")

@app.route('/predict_api', methods = ["POST"])

def predict_api():
    data = request.json["data"]
 
 
    data_frame = pd.DataFrame.from_dict(data, orient="columns")
    print(data_frame)

    data_cleaned = pipe.data_cleaning(data_frame)
    print(f"data_cleaned is {data_cleaned}")
    data_features_added = pipe.feature_creation(data_cleaned)
    print(f"feature added is {data_features_added}")
    data_prepared = pipe.data_preparation(data_features_added)
    print(f"feature prepared is {data_prepared}")
    prediction = pipe.predict(data_prepared).tolist()


    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=5000)