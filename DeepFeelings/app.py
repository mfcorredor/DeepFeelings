import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import emoji
import plotly.express as px
from PIL import Image
from visualization import pie_chart, timeline_chart, word_cloud
#from sentiment_analysis import get_sentiment
from LDA_clustering import get_topics_LDA_model


# page config
# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

# title image
title_image = Image.open("images/deep-learning-large (1).jpg")
st.image(title_image)

#titles and input buttons
new_title = '<p style="font-family:sans-serif; color:#C6CDD4; font-size: 25px;">Check out what people is thinking about your brand and products!</p>'
input_1 = '<p style="font-family:sans-serif; color:#C6CDD4; font-size: 20px;">Insert your product ID</p>'
input_2 = '<p style="font-family:sans-serif; color:#C6CDD4; font-size: 20px;">Insert the name of your brand</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.write("**  **")
st.markdown(input_1, unsafe_allow_html=True)
prduct = st.text_input('')
st.write(" ")
st.markdown(input_2, unsafe_allow_html=True)
brand = st.text_input(' ')

if st.button("Get report"):
    #data = get_sentiment(product, brand)
    data = pd.read_csv("../raw_data/sentiment_tweets_apple.csv")
    data['date'] = pd.to_datetime(data['date'])
    topics_neg, topics_pos = get_topics_LDA_model(data)

    fig1 = pie_chart(data)
    fig2 = word_cloud(topics_neg[0])
    fig3 = timeline_chart(data)

    # linecount
    line_count = st.slider('Select a line count', 1, 10, 3)
    head_data = data.head(line_count)
    head_data

    # buttons to dispay numbers (number of reviews, number of positive reviews, etc.)

    #columns creation
    columns = st.columns(2)
    first_column = columns[0].pyplot(fig1)

    # markdowns to add space
    st.markdown("""
    """)
    st.markdown("""
    """)

    with columns[1]:
        st.markdown("""# Most common words used in the reviews or tweets""")
        second_column = columns[1].pyplot(fig2)

    st.pyplot(fig3)

CSS="""
    img{
        width:200vh;
    }
    .css-ocqkz7{
        margin-top:100px
    }
"""
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)
