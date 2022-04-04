#30days of Streamlit

#packages
import imp
import streamlit as st

from nltk.tokenize import word_tokenize
from textblob import TextBlob
from textblob import Word

import spacy
from spacy import displacy
nlp_pipe = spacy.load("en_core_web_sm")
#different tabs performing the tasks (functions)

#tokenizer
def tokenizer(text):
    tokens = []
    for each_post in text:
        tokens.append(word_tokenize(each_post))

    return tokens


#lemmatize
def lemmatizer(text):
    text = ''.join(text)
    post_blob = TextBlob(text)
    tokens = []
    for each_token in post_blob.tokens:
        tok = each_token
        tok = Word(tok).lemmatize(pos="v")
        tok = Word(tok).lemmatize(pos="n")
        tokens.append(tok)
    return (tokens)


#part of speech tagger
def fun_pos(text, partOfSpeech):

    return text

#named entity recognizer = loads txt file / copy text

def fun_named_entity(text):
    text = ''.join(text)
    doc = nlp_pipe(text) 
    return displacy.render(doc, style='ent')



#grammar correction tool
def fun_sentence_correct(text):
    text = ''.join(text)
    return TextBlob(text).correct()

#calculate sentiment
def fun_sentiment(text):
    text = ''.join(text)
    text = TextBlob(text)
    sentiments = []
    for each_sentence in text.sentences:
        sentiments.append(each_sentence.sentiment)
    return sentiments




st.set_page_config(layout='wide')

with st.sidebar:
    st.markdown("## Simple NLP Tools")
    st.markdown("this project was built as part of the **#30DaysofStreamlit** in April 2022.")
    st.markdown("I made use of the following packages:")
    st.markdown("- [nltk](https://www.nltk.org/): For tokenization")
    st.markdown("- [spaCy](https://spacy.io/usage): For named-entity recognition")
    st.markdown("- [TextBlob](https://textblob.readthedocs.io/en/dev/#): For lemmatization, sentence correction and sentence subjectivity/polarity")
    st.markdown("*By: Ebenezer Agbozo (eagbozo@urfu.ru | agbozo1@gmail.com)*")
col1, col2 = st.columns(2)
with col1:
    st.title("Exploring Basic NLP Tasks")
    
    content = [st.text_area("Enter Text Here", value="")]

    choices = st.selectbox("Select the NLP Task", 
    ('Tokenization', 'Lemmatization', 'Named Entity Recognizer', "Sentence Correction", "Sentiment"))

    if(choices == "Tokenization"):
        if(len(content) > 0):
            st.write("**Tokens:** ",tokenizer(content)) 
    
    elif(choices == "Lemmatization"):
        if(len(content) > 0):
            st.write("**Lemma (noun/verb):** ",lemmatizer(content)) 
    
    elif(choices == "Named Entity Recognizer"):
        if(len(content) > 0):
            st.write("**Named Entity Recognizer:** ",fun_named_entity(content), unsafe_allow_html=True)

    elif(choices == "Sentence Correction"):
        if(len(content) > 0):
            st.write("**Grammar Correction:** ",fun_sentence_correct(content)) 
    
    elif(choices == "Sentiment"):
        if(len(content) > 0):
            st.write("**Sentiment Score (0: Polarity. 1: Subjectivity):** ",fun_sentiment(content)) 
            

with col2:
    st.text('')
