# Create API of ML model using flask

'''
This code takes the JSON data while POST request an performs the prediction using loaded model and returns
the results in JSON format.
'''

# Import libraries
import numpy as np
from flask import Flask, request, jsonify
import pickle
import os

app = Flask(__name__)

# Load the model

model_path = os.path.join('static', 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

vectorizer_path = os.path.join('static', 'vectorizer.pkl')
vectorizer = pickle.load(open(vectorizer_path, 'rb'))


@app.route('/api', methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)

    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict(vectorizer.transform([data['url']]))

    # Take the first value of prediction
    output = prediction[0]

    return jsonify(str(bool(output)))


@app.route('/')
def hello_world():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
