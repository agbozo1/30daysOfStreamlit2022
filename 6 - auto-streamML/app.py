import streamlit as st
import pandas as pd
import os
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
#from pycaret.classification import setup, compare_models, pull, save_model
import pycaret.classification as ml_classify
import pycaret.regression as ml_regress

st.write("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400&display=swap');
html, body, [class*="css"]  {
   font-family: 'Fascinate', cursive;
}
img {
    align:center;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.freepik.com/premium-photo/calendar-3d-icon_307432-49.jpg?w=2000", width=120)
    st.title("AutoML Stream")

    choice = st.radio("Navigation", ['Data Upload', 'Profiling', 'ML', 'Download'])
    st.info("An Automated ML Pipeline Built on Streamlit, Pandas Profiling and PyCaret - Inspired by Nicholas Renotte (https://github.com/nicknochnack)")

if os.path.exists('data/original_data.csv'):
    df = pd.read_csv('data/original_data.csv', index_col=None)


if choice == "Data Upload":
    st.title("📥 Data Loader")
    file = st.file_uploader('Dataset Goes Here')

    if file:
        df = pd.read_csv(file, index_col=None)
        df.to_csv('data/original_data.csv', index=None)
        st.dataframe(df)

if choice == "Profiling":
    st.title("📈 Exploratory Data Analysis")
    profile_report = df.profile_report()
    st_profile_report(profile_report)


if choice == "ML":
    st.title("🚀 Apply ML")
    ml_technique = st.radio('ML Method:', ['Classification','Regression'])

    target = st.selectbox('Select Target Column', df.columns)
    
    if st.button('Train Model'):

        #CLASSIFICATION TECHNIQUE SELECTED
        if ml_technique == "Classification":
            ml_classify.setup(df, target=target, silent=True)   
            setup_df = ml_classify.pull()

            st.info("Experiment Settings")
            best_model = ml_classify.compare_models()
            compare_df = ml_classify.pull()
            
            st.info("ML Model")
            st.dataframe(compare_df)
            best_model

            ml_classify.save_model(best_model,'model/best_model_classification')
        
        #REGRESSION TECHNIQUE SELECTED
        if ml_technique == "Regression":
            ml_regress.setup(df, target=target, silent=True)   
            setup_df = ml_regress.pull()

            st.info("Experiment Settings")
            best_model = ml_regress.compare_models()
            compare_df = ml_regress.pull()
            
            st.info("Regression-Based ML Model")
            st.dataframe(compare_df)
            best_model

            ml_regress.save_model(best_model,'model/best_model_regression')

if choice == "Download":
    st.title("💾 Model Downloader")
    if not os.path.exists('model/best_model_classification.pkl') or os.path.exists('model/best_model_regression.pkl'):
        st.write("No Model Yet. Come Back Later!")
    else:
        with open("model/best_model.pkl", 'rb') as f:
            st.download_button("Download Model", f, "trained_model.pkl")
