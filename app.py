from __future__ import division, print_function
# coding=utf-8
import os
import json
import datetime
import config
import model_datastore
import storage
import numpy as np
from pred_re import model_predict

# Flask utils
from flask import current_app, Flask, redirect, url_for, request, render_template
from flask import jsonify
from flask_pymongo import PyMongo # to connect mongoDB
from bson.objectid import ObjectId # ObjectID used in mongoDB
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

class JSONEncoder(json.JSONEncoder):                           
    ''' extend json-encoder class'''
    def default(self, o):                               
        if isinstance(o, ObjectId):
            return str(o)                               
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    return public_url

# Define a flask app
app = Flask(__name__)
app.config.from_object(config)

# Setup the data model.
with app.app_context():
    model_datastore.init_app(app)

# Configure MongoDB 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/image_classification_flask'

# Define a mongo reference
mongo = PyMongo(app)



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
        # # Get the file from post request
        # f = request.files['file']

        # # Save the file to ./uploads
        # basepath = os.path.dirname(__file__)
        # file_path = os.path.join(
        #     basepath, 'uploads', secure_filename(f.filename))
        # f.save(file_path)

        data = request.form.to_dict(flat=True)

        # If an image was uploaded, update the data to point to the new image.
        image_url = upload_image_file(request.files['file'])
        if image_url:
            data['url'] = image_url
        model_datastore.create(data)

        # Predict the category and return the result
        result = model_predict(None, image_url, 5, 'model', 'categories.txt')
        os.environ['URL'] = image_url
        return jsonify(result)
    return None

@app.route('/choose_result', methods=['GET', 'POST'])
def choose_result():
    if request.method == 'POST':
        result = request.form['result']
        correct_result = request.form['correct_result']
        # put result and path into database
        insertion = mongo.db.images.insert_one({
            'url': os.environ['URL'],
            'result': result,
            'correct_result': correct_result,
        })
    return redirect('/')

if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
