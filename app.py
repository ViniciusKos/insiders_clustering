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
 
 
    data_frame = pd.DataFrame.from_dict(data)


    data_cleaned = pipe.data_cleaning(data_frame)
    data_features_added = pipe.feature_creation(data_cleaned)
    data_prepared = pipe.data_preparation(data_features_added)
    prediction = pipe.predict(data_prepared)


    print(data_frame)
    print(f"prediction is {prediction}")
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug = True)