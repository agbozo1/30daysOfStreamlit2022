import imp
import cv2
import numpy as np
from PIL import Image, ImageOps

import streamlit as st
import tensorflow as tf


def emotion_classifier(image_file, model_location):

    #image pre-processing
    image = ImageOps.fit(image_file, (224, 224), Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    
    image_data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image_data[0] = normalized_image_array

    #predict
    emotion_model = tf.keras.models.load_models(model_location)
    prediction = emotion_model.predict(image_data)

    return np.argmax(prediction)

#teachable machine

st.set_page_config(layout='wide')
with st.sidebar:
    st.markdown("## Simple Emotion Detection App")
    st.markdown("this project was built as part of the **#30DaysofStreamlit** in April-May 2022.")
    st.markdown("- Liu Xiaozhi")
    st.markdown("- Sun Xu")
    st.markdown("- Avinash Kumar")
    st.markdown("- Al-Samarrai Safa Shakir Awad")
    st.markdown("**_Supervised By: Ebenezer Agbozo_**")
    st.markdown("**_(eagbozo@urfu.ru | agbozo1@gmail.com)_**")
    st.markdown("**_Ural Federal University_**")
col1, col2 = st.columns(2)
with col1:
    switch = st.radio("", ("Off", "On"))

    if switch == "On":
        st.success("Camera On") #notification
        cam = cv2.VideoCapture(0)
        st_frame = st.empty()
        ret, img = cam.read()
        while ret:
            ret, img = cam.read()
            if ret:
                st_frame.image(img, channels='BGR')
        
        
    else:
        st.warning("Camera Off")
        cam = cv2.VideoCapture(0)
        cam.release()
        