import streamlit as st
import numpy as np 
import warnings
import os
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import pandas as pd
import code.preparation as prep
import code.visualization as viz    
from PIL import Image
import joblib
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import img_to_array
import time

np.random.seed(123)

header = st.container()
dataset = st.container()
features = st.container()
modeltraining = st.container()

with header:
    st.title('Welcome to the Pneumonia Classification Project')
    st.markdown(
    """
    <style>
   .sidebar .sidebar-content {
        background: #FFED91;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    st.markdown("The number of Pneumonia cases increased in the last few years with 1.5 million ER visits and 2 million deaths indicating around 16% increase. The goal of our project is to build a image classification model that can correctly identify between x-rays of infected and healthy lungs so we can lower these numbers. It's important that our model has high accuracy.")



with dataset:
    
    st.header("Data Understanding")
    
    st.markdown("Our data comes from Mendeley Data, it contains a few thousand images Chest X-Ray described and analyzed in 'Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning'. The images are split into a training set and a testing set of independent patients. Images are labeled as (disease)-(randomized patient ID)-(image number by this patient). We are going to be classifying whether the images fall into the two classes either 'NORMAL' or 'PNEUMONIA'.")


    
with features:
        
    st.header('Data Preview')
    st.markdown('A random selection of images from the dataset.')
    first_img = image.load_img('images/data_preview.png')
    st.image(first_img)
    
    scd_img = image.load_img('images/class_imbalance.png')
    st.sidebar.image(scd_img)

with modeltraining:
    st.header('Model Predictor')
    st.markdown('Here we can test the model to see how it performs. Please choose from the list of images down below, either NORMAL or PNEUMONIA and the model with try to classify that image.')
    fig = plt.figure()
    

    path = st.selectbox("Choose File", options=['data/chest_xray/test/PNEUMONIA/person1_virus_11.jpeg', 'data/chest_xray/test/PNEUMONIA/person1_virus_12.jpeg', 'data/chest_xray/test/PNEUMONIA/person1_virus_13.jpeg', 'data/chest_xray/test/PNEUMONIA/person137_bacteria_655.jpeg', 'data/chest_xray/test/PNEUMONIA/person10_virus_35.jpeg', 'data/chest_xray/test/PNEUMONIA/person1_virus_8.jpeg', 'data/chest_xray/test/PNEUMONIA/person1_virus_9.jpeg', 'data/chest_xray/test/NORMAL/IM-0001-0001.jpeg', 'data/chest_xray/test/NORMAL/IM-0081-0001.jpeg', 'data/chest_xray/test/NORMAL/IM-0005-0001.jpeg', 'data/chest_xray/test/NORMAL/IM-0006-0001.jpeg', 'data/chest_xray/test/NORMAL/IM-0070-0001.jpeg', 'data/chest_xray/test/NORMAL/IM-0003-0001.jpeg', 'data/chest_xray/test/NORMAL/IM-0101-0001.jpeg'], index=0)

    img = image.load_img(path, target_size=(260, 260))
    st.image(img, caption='Image Uploaded', use_column_width=True)
    plt.imshow(img)
    plt.axis("off")
    time.sleep(1)
    st.success('Classified')

    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    model = load_model('Models/best_model_accuracy.h5', compile=False)
    predictions = model.predict(img)
    st.write(predictions)
    class_names = [
              'Normal',
              'Pneumonia']

    scores = tf.nn.softmax(predictions[0]).numpy()
    results = {
              'Normal': 0,
              'Pneumonia': 0
    }


    result = f"Model classified image as - {class_names[np.argmax(scores)]} - with a { (100 * np.max(scores)).round(2) } % confidence."
    st.write(result)


