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
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the model

model_path_tld = os.path.join('static', 'model_tld.pkl')
model_tld = pickle.load(open(model_path_tld, 'rb'))

vectorizer_path_tld = os.path.join('static', 'vectorizer_tld.pkl')
vectorizer_tld = pickle.load(open(vectorizer_path_tld, 'rb'))

model_path_full_url = os.path.join('static', 'model_full_url.pkl')
model_full_url = pickle.load(open(model_path_full_url, 'rb'))

vectorizer_path_full_url = os.path.join('static', 'vectorizer_full_url.pkl')
vectorizer_full_url = pickle.load(open(vectorizer_path_full_url, 'rb'))


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

    original_url = str(data['url'])
    stripped_url = original_url.replace('https://', '').replace('http://', '')

    tld_accuracy = get_tld_accuracy(stripped_url)
    full_url_accuracy = get_full_url_accuracy(stripped_url)

    prediction = None
    model = None
    accuracy = None
    if tld_accuracy > full_url_accuracy:
        prediction = model_tld.predict(vectorizer_tld.transform([stripped_url]))[0]
        model = 'Top Level Domain Model'
        accuracy = tld_accuracy

    elif tld_accuracy <= full_url_accuracy:
        prediction = model_full_url.predict(vectorizer_full_url.transform([stripped_url]))[0]
        model = 'Full URL Model'
        accuracy = full_url_accuracy

    if str(prediction) == '0':
        prediction = False
    else:
        prediction = True

    return_data = {}
    return_data.update({'model': model})
    return_data.update({'accuracy': str(accuracy)})
    return_data.update({'prediction': str(prediction)})
    return_data = json.dumps(return_data)

    return jsonify(return_data)


@app.route('/')
def hello_world():
    return "Hey there! You may want to try hitting the API instead of this URL. More info can be found at linked in"


def get_tld_accuracy(url):
    probability = model_tld.predict_proba(vectorizer_tld.transform([url]))
    percent_true = float(probability[0][0])
    percent_false = float(probability[0][1])

    accuracy = percent_true - percent_false
    if accuracy < 0:
        accuracy = accuracy * -1

    return accuracy


def get_full_url_accuracy(url):
    probability = model_full_url.predict_proba(vectorizer_full_url.transform([url]))
    percent_true = float(probability[0][0])
    percent_false = float(probability[0][1])

    accuracy = percent_true - percent_false
    if accuracy < 0:
        accuracy = accuracy * -1

    return accuracy


if __name__ == '__main__':
    app.run(port=5000, debug=True)
