from __future__ import division, print_function
# coding=utf-8
import os
import config
import model_mongodb
import storage
import numpy as np
from pred_re import model_predict

# Flask utils
from flask import current_app, Flask, redirect, url_for, request, render_template
from flask import jsonify
from bson.objectid import ObjectId # ObjectId used in mongoDB
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

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
    model_mongodb.init_app(app)

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

@app.route('/data')
def data():
    results1 = model_mongodb.find('result', 'result1')
    results2 = model_mongodb.find('result', 'result2')
    results3 = model_mongodb.find('result', 'result3')
    results4 = model_mongodb.find('result', 'result4')
    results5 = model_mongodb.find('result', 'result5')
    results6 = model_mongodb.find('result', 'none')
    results_count = [results1.count(), results2.count(), results3.count(), results4.count(), results5.count(), results6.count()]
    return jsonify(results_count)

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Upload the image in request to Google Cloud
        image_url = upload_image_file(request.files['file'])
    
        # Predict the category and return the result
        result = model_predict(None, image_url, 5, 'model', 'categories.txt')
        
        # store url, results into MongoDB
        data = request.form.to_dict(flat=True) #???
        if image_url:
            data['url'] = image_url
            data['result1'] = result[0]
            data['result2'] = result[1]
            data['result3'] = result[2]
            data['result4'] = result[3]
            data['result5'] = result[4]
        image_id = model_mongodb.create(data)

        # store the current id into os.environ
        os.environ['ID'] = str(image_id)

        return jsonify(result)
    return None

@app.route('/choose_image', methods=['GET', 'POST'])
def choose_image():
    if request.method == 'POST':
        category = request.form['image_category']
        
        #get image urls of result1 from mongoDB
        image_list = list(model_mongodb.find('result', category))
        urls = []
        for image in image_list:
            urls.append(image['url'])
        return render_template('accuracy.html', urls = urls )
    return None

@app.route('/choose_result', methods=['GET', 'POST'])
def choose_result():
    if request.method == 'POST':
        result = request.form['result']
        
        # figure out the correct result based on the result
        if result == 'none':
            correct_result = request.form['correct_result']
        elif result == 'result1':
            correct_result = model_mongodb.read(os.environ['ID'])['result1']
        elif result == 'result2':
            correct_result = model_mongodb.read(os.environ['ID'])['result2']
        elif result == 'result3':
            correct_result = model_mongodb.read(os.environ['ID'])['result3']
        elif result == 'result4':
            correct_result = model_mongodb.read(os.environ['ID'])['result4']
        elif result == 'result5':
            correct_result = model_mongodb.read(os.environ['ID'])['result5']

        # put result and url into database
        model_mongodb.update(
            {
                'result': result,
                'correct_result': correct_result,
            },
            ObjectId(os.environ['ID'])
        )
    return redirect('/')


if __name__ == '__main__':
    # Serve the app with gevent
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
