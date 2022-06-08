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
import base64

# page config, use the full page instead of a narrow central column
st.set_page_config(layout="wide")


#background
def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "gif"
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack('../raw_data/video_20_sec.gif')

# title image
#title_image = Image.open("images/deep-learning-large (1).jpg")
#st.image(title_image)

#titles and input buttons
new_title = '<p style="font-family:sans-serif; font-weight:bold; color:white; font-size: 120px;">DeepFeelings</p>'
input_1 = '<p style="font-family:sans-serif; font-weight:bold; color:white; font-size: 25px;">Insert product name</p>'
input_2 = '<p style="font-family:sans-serif; font-weight:bold; color:white; font-size: 25px;">Insert brand name</p>'
st.markdown(new_title, unsafe_allow_html=True)
st.write(" ")
st.markdown(input_1, unsafe_allow_html=True)
product = st.text_input('')
st.write(" ")
st.markdown(input_2, unsafe_allow_html=True)
brand = st.text_input(' ')

#topics_neg_sneakers = 'look wear comfortable fake small little returned size fit feel tight quality'
topics = pd.read_csv('../raw_data/topics_neg.csv', index_col='brand_product')

if st.button("Get report"):
    brand = brand.lower()
    product = product.lower()
    if brand != '' and product != '':
        file_list = [f"../raw_data/sentiment_amz_{product}.csv",
                    f"../raw_data/sentiment_tw_{brand}.csv"]
        csv_list = [pd.read_csv(file) for file in file_list]
        data = pd.concat(csv_list, ignore_index=True)
        data_amz = pd.read_csv(file_list[0])
        data_amz['date'] = pd.to_datetime(data['date'])
        topic = topics['negative_topics'][brand]
        fig3 = timeline_chart(data_amz)
    elif brand != '':
        data = pd.read_csv(f"../raw_data/sentiment_tw_{brand}.csv")
        topic = topics['negative_topics'][f"{brand}_tw"]
    elif product != '':
        data = pd.read_csv(f"../raw_data/sentiment_amz_{product}.csv")
        data['date'] = pd.to_datetime(data['date'])
        topic = topics['negative_topics'][f"{product}_amz"]
        fig3 = timeline_chart(data)



    #topics_neg, topics_pos = get_topics_LDA_model(data)


    fig1 = pie_chart(data)
    fig2 = word_cloud(topic)

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
    button{
        background-color: white !important;
        width: 180px !important;
        height: 51px !important;
        font-size: 21px !important;
}
    }
"""
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)
