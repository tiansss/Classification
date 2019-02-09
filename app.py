from __future__ import division, print_function
# coding=utf-8
import sys
import os
import json
import datetime
import glob
import re
import numpy as np
from pred_re import model_predict

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from flask import jsonify
from flask_pymongo import PyMongo # to connect mongoDB
from bson.objectid import ObjectId # ObjectID used in mongoDB
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Configure MongoDB 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/image_classification_flask'

# Define a mongo reference
mongo = PyMongo(app)



# file path environment variable name
FILEPATH = 'FILEPATH'

print('Model loaded. Check http://127.0.0.1:5000/')

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/info')
def info():
    #information page
    return render_template('info.html')

@app.route('/accuracy')
def accuracy():
    #information page
    return render_template('accuracy.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        result = model_predict(file_path, 5, 'model', 'categories.txt')
        os.environ[FILEPATH] = file_path
        return jsonify(result)
    return None

@app.route('/choose_result', methods=['GET', 'POST'])
def choose_result():
    if request.method == 'POST':
        result = request.form['result']
        correct_result = request.form['correct_result']
        # put result and path into database
        insertion = mongo.db.images.insert_one({
            'path': os.environ[FILEPATH],
            'result': result,
            'correct_result': correct_result,
        })
    return redirect('/')

if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
