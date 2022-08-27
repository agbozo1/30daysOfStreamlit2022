
import cv2
import os
import numpy as np
from skimage.filters import gaussian
import streamlit as st
from PIL import Image, ImageColor
import functions as fxn


#inspired by https://pavankunchalapk.medium.com/virtual-makeup-app-using-streamlit-and-opencv-b1271b8e2d01
#https://github.com/Pavankunchala/Virtual_Makeup_Streamlit/blob/main/app.py
#https://github.com/zllrunning/face-parsing.PyTorch

print(fxn.test())

st.title('Virtual Makeup')

st.sidebar.title('Virtual Makeup')
st.sidebar.subheader('Parameters')
table = {
        'hair': 17,
        'upper_lip': 12,
        'lower_lip': 13,
        
    }



img_file_buffer = st.sidebar.file_uploader("Upload an image", type=[ "jpg", "jpeg",'png'])

if img_file_buffer is not None:
    image = np.array(Image.open(img_file_buffer))
    demo_image = img_file_buffer

else:
    demo_image = "demo.jfif"
    image = np.array(Image.open(demo_image))



#st.subheader('Original Image')
st.image(image,use_column_width = True)

parts = [table['hair'], table['upper_lip'], table['lower_lip']]

hair_color = st.sidebar.color_picker('Pick the Hair Color', '#000')
hair_color = ImageColor.getcolor(hair_color, "RGB")

lip_color = st.sidebar.color_picker('Pick the Lip Color', '#edbad1')
lip_color = ImageColor.getcolor(lip_color, "RGB")

colors = [hair_color, lip_color]

sharpener = st.sidebar.slider("Sharpen Image:")
st.markdown(sharpener)

