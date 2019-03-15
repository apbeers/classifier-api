# Create API of ML model using flask

'''
This code takes the JSON data while POST request an performs the prediction using loaded model and returns
the results in JSON format.
'''

# Import libraries
import socket
from flask import Flask, request, jsonify
import pickle
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the model

model_path = os.path.join('static', 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

vectorizer_path = os.path.join('static', 'vectorizer.pkl')
vectorizer = pickle.load(open(vectorizer_path, 'rb'))


@app.route('/api', methods=['POST'])
def predict():

    # Get the data from the POST request.
    data = request.get_json(force=True)

    if not data['ip_for_url']:
        try:
            data['ip_for_url'] = socket.gethostbyname(data['url'])
        except socket.gaierror as e:
            print('Error looking up url: {0}'.format(e))

    if data['white_listed_ips'] and data['ip_for_url'] in data['white_listed_ips']:
        return jsonify('IP for url is whitelisted: {0}'.format(data['ip_for_url']))

    if data['black_listed_ips'] and data['ip_for_url'] in data['black_listed_ips']:
        return jsonify('IP for url is blacklisted {0}'.format(data['ip_for_url']))

    print(data)

    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict(vectorizer.transform([data['url']]))

    return jsonify(str(bool(prediction[0])))


@app.route('/')
def hello_world():
    return "Hey there! You may want to try hitting the API instead of this URL. More info can be found at linked in"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
