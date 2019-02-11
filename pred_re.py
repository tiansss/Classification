import os
import six
if six.PY2:
    import urllib
else:
    import urllib.request
import tensorflow as tf
import numpy as np
from tensorflow.python.saved_model import tag_constants

def add_jpeg_decoding(h, w, d):
    input_height, input_width, input_depth = (h, w, d)
    jpeg_data = tf.placeholder(tf.string, name='DecodeJPGInput')
    decoded_image = tf.image.decode_jpeg(jpeg_data, channels=input_depth)
    # Convert from full range of uint8 to range [0,1] of float32.
    decoded_image_as_float = tf.image.convert_image_dtype(decoded_image,
                                                            tf.float32)
    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
    resize_shape = tf.stack([input_height, input_width])
    resize_shape_as_int = tf.cast(resize_shape, dtype=tf.int32)
    resized_image = tf.image.resize_bilinear(decoded_image_4d,
                                            resize_shape_as_int)
    return jpeg_data, resized_image

def read_categories(dir):
    ans = []
    f = open(dir)
    line = f.readline()
    while line:
        cate = line.split('.')
        ans.append(cate[1][:-1])
        line = f.readline()
    f.close()
    return ans

def model_predict(image_path, image_url, max_size, model_path, categories_path):
    categories = read_categories(categories_path)
    img_size = 299
    num_channels = 3
    jpeg_data_tensor, decoded_image_tensor = add_jpeg_decoding(img_size, img_size, num_channels)
    sess = tf.Session()

    if not (image_path == None):
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    else:
        if six.PY2:
            image_data = urllib.urlopen(image_url).read()
        else:   
            image_data = urllib.request.urlopen(image_url).read()
    resized_input_values = np.array(sess.run(decoded_image_tensor, {jpeg_data_tensor: image_data}))

    tf.saved_model.loader.load(sess, [tag_constants.SERVING], model_path)
    x = tf.get_default_graph().get_tensor_by_name('Placeholder:0')
    z = tf.get_default_graph().get_tensor_by_name('final_result:0')

    pred = tf.nn.softmax(z)
    res = sess.run(pred, {x: resized_input_values})[0]
    res_np = np.array(res)
    n_largest_i = res_np.argsort()[-max_size:][::-1]
    n_largest_cat = []
    for index in n_largest_i:
        n_largest_cat.append(categories[index])
    return n_largest_cat