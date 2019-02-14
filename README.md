# image_classification_flask
**An image classification web application built by Flask, Google Cloud, MongoDB and TensorFlow.**
![screenshot1]()

## Introduction
* This is a Flask web application based on our project [https://github.com/tiansss/Image-Classification](https://github.com/tiansss/Image-Classification). 

* Dataset: [Caltech256](http://www.vision.caltech.edu/Image_Datasets/Caltech256/). 

* Training Model: We retrained a model which was trained by ImageNet(a very large image set) using Tensorflow. 

* Web: We used [Flask](http://flask.pocoo.org/) which is a microframework for Python and based on [Werkzeug](http://werkzeug.pocoo.org/) and [Jinja2](http://jinja.pocoo.org/). 

* Cloud: We used [Google Cloud Storage](https://cloud.google.com/storage/) to store all images uploaded.

* Database: We used [MongoDB](https://www.mongodb.com/) as our database, which is to store image urls, predicting results, and correct results. We used [PyMongo](https://api.mongodb.com/python/current/) to work with MongoDB from Python.

* Visual: We displays bar chart and pie chart for our result accuracy using [Chart.js](https://www.chartjs.org/) library. A little [jQuery](https://jquery.com/) and [bootstrap](https://getbootstrap.com/) too.


## How to run
### Modify config.py with your own Google Cloud and MongoDB information.
### Install requirements
```
$ pip install -r requirements.txt
```
### Run the application
```
$ python app.py
```
### Open http://127.0.0.1:5000/


