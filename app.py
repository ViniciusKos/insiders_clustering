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
    print(data)
    #print(data.__class__)
    #print(np.array(list(data.values())).reshape(1, -1))
    data_frame = pd.DataFrame.from_dict(data)
    print(data_frame)

    output = pipe.data_cleaning(data_frame)


    print(output[0])
    return jsonify(output[0])

if __name__ == "__main__":
    app.run(debug = True)