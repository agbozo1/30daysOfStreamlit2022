#in cmd enter
#python
#import cv2
#print(cv2.__file__)
#get python location and copy data folder to cascades folder in this project

import numpy as np 
import cv2
import streamlit as st


FACE_CASCADE = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

cam = cv2.VideoCapture(0)

switch = st.radio("", ("Off", "On"))

if switch == "On":
    #

    #frame by frame capture
    ret, frame = cam.read()
    while(cam.isOpened()):
    #show image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.video(frame)
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

else:
#escape
    cam.release()
    cv2.destroyAllWindows()




#remember
#https://medium.com/mlearning-ai/live-webcam-with-streamlit-f32bf68945a4
#https://dev.to/whitphx/build-a-web-based-real-time-computer-vision-app-with-streamlit-57l2
#https://discuss.streamlit.io/t/streamlit-webcam-stream-processing-using-opencv-python-and-tensorflow/17753