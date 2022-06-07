import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import emoji
import plotly.express as px
from PIL import Image
from visualization import pie_chart, timeline_chart, word_cloud
#from sentiment_analysis import get_sentiment
from LDA_clustering import get_topics_LDA_model, preproc_LDA


# page config
# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

#video background
video_html = """
		<style>

		#myVideo {
		  position: fixed;
		  right: 0;
		  bottom: 0;
		  min-width: 100%;
		  min-height: 100%;
		}

		.content {
		  position: fixed;
		  bottom: 0;
		  background: rgba(0, 0, 0, 0.5);
		  color: #f1f1f1;
		  width: 100%;
		  padding: 20px;
		}

		</style>
		<video autoplay muted loop id="myVideo">
		  <source src="https://www.youtube.com/watch?v=j22DmsZEv30")>
		  Your browser does not support HTML5 video.
		</video>
        <video controls>


"""

st.markdown(video_html, unsafe_allow_html=True)

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
product = st.text_input('')
st.write(" ")
st.markdown(input_2, unsafe_allow_html=True)
brand = st.text_input(' ')

topics_neg_sneakers = 'look wear comfortable fake small little returned size fit feel tight quality'

if st.button("Get report"):

    if brand != '' and product != '':
        file_list = ["../raw_data/sentiment_amz_{product}.csv",
                    "../raw_data/sentiment_tw_{brand}.csv"]
        csv_list = [pd.read_csv(file) for file in file_list]
        data = pd.concat(csv_list, ignore_index=True)
        data_amz = pd.read_csv(file_list[0])
        data_amz['date'] = pd.to_datetime(data['date'])
        fig3 = timeline_chart(data_amz)
    elif brand != '':
        data = pd.read_csv(f"../raw_data/sentiment_tw_{brand}.csv")
    elif product != '':
        data = pd.read_csv(f"../raw_data/sentiment_amz_{product}.csv")
        data['date'] = pd.to_datetime(data['date'])
        fig3 = timeline_chart(data)



    #topics_neg, topics_pos = get_topics_LDA_model(data)


    fig1 = pie_chart(data)
    fig2 = word_cloud(topics_neg_sneakers)

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
    if product != '':

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
