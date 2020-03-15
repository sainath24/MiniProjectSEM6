from flask import Flask,request,jsonify
import numpy as np
import base64
import cv2


import tensorflow as tf
import zipfile
import urllib.request
import shutil
import glob
# import tqdm
import random
import os
import sys
import os
import sys
import time
import numpy as np
import skimage.io
import keras.backend
import json
# Download and install the Python COCO tools from https://github.com/waleedka/coco
# That's a fork from the original https://github.com/pdollar/coco with a bug
# fix for Python 3.
# I submitted a pull request https://github.com/cocodataset/cocoapi/pull/50
# If the PR is merged then use the original repo.
# Note: Edit PythonAPI/Makefile and replace "python" with "python3".
#
# A quick one liner to install the library
# !pip install git+https://github.com/waleedka/coco.git#subdirectory=PythonAPI

from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval
from pycocotools import mask as maskUtils
import coco #a slightly modified version

ROOT_DIR = os.getcwd()

sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils

PRETRAINED_MODEL_PATH = os.path.join(ROOT_DIR,"weight.h5")
LOGS_DIRECTORY = os.path.join(ROOT_DIR, "logs")
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
# IMAGE_DIR = os.path.join(ROOT_DIR, "data", "test")

global graph


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 41  # 1 Background + 1 Building
    # IMAGE_MAX_DIM=512
    # IMAGE_MIN_DIM=512
    NAME = "food"
    # DETECTION_MIN_CONFIDENCE=0

config = InferenceConfig()
config.display()
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

model_path = PRETRAINED_MODEL_PATH

model.load_weights(model_path, by_name=True)
K = keras.backend.backend()
#if K=='tensorflow':
#    keras.backend.set_image_dim_ordering('tf')



# model_path = PRETRAINED_MODEL_PATH

# # or if you want to use the latest trained model, you can use :
# # model_path = model.find_last()[1]

# model.load_weights(model_path, by_name=True)

# model.keras_model._make_predict_function()


class_names = ['BG', 'potatoes-steamed', 'chips-french-fries', 'mixed-vegetables', 'mixed-salad-chopped-without-sauce', 'leaf-spinach', 'salad-leaf-salad-green', 'avocado', 'french-beans', 'cucumber', 'sweet-pepper', 'tomato', 'zucchini', 'carrot', 'broccoli', 'apple', 'banana', 'strawberries', 'hard-cheese', 'cheese', 'rice', 'pasta-spaghetti', 'bread-whole-wheat', 'bread-wholemeal', 'bread-white', 'chicken', 'egg', 'butter', 'jam', 'dark-chocolate', 'tea', 'espresso-with-caffeine', 'coffee-with-caffeine', 'white-coffee-with-caffeine', 'water', 'water-mineral', 'wine-red', 'wine-white', 'tomato-sauce', 'mayonnaise', 'pizza-margherita-baked']

# In our case, we have 1 class for the background, and 1 class for building

id_category = [0, 1010, 1013, 1022, 1026, 1032, 1040, 1056, 1058, 1061, 1068, 1069, 1070, 1078, 1085, 1151, 1154, 1163, 1310, 1311, 1468, 1505, 1554, 1565, 1566, 1788, 2022, 2053, 2099, 2131, 2498, 2504, 2512, 2521, 2578, 2580, 2618, 2620, 2738, 2750, 2939]




app = Flask(__name__)


@app.route('/')
def home():
    return 'HOME PAGE'

@app.route('/uploadmeal', methods=["GET","POST"])
def uploadMeal():
    global model
    content = request.get_json()
    print(content)
    picnp = np.fromstring(base64.b64decode(content['pic']), dtype=np.uint8)
    img = cv2.imdecode(picnp, 1)

    cv2.imwrite("food.jpg",img)

    f="food.jpg" #specify file name here 
    image = skimage.io.imread(f)

    # model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # model_path = PRETRAINED_MODEL_PATH

    # model.load_weights(model_path, by_name=True)

    # or if you want to use the latest trained model, you can use :
    # model_path = model.find_last()[1]
    
    # model.keras_model._make_predict_function()

    results = model.detect([image], verbose=1)
    # print(class_names[results[0]['class_ids'][0]])

    food_list = []

    for p in results[0]['class_ids']:
        food_list.append(class_names[p])


    

    response ={}
    response['food'] = food_list
    print(response)
    return jsonify(response)

if __name__ == '__main__':

    app.run(host = '192.168.43.213', port = '4444')
