import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import emoji
import plotly.express as px
from PIL import Image
from data import get_data
from visualization import pie_chart, timeline_chart, word_cloud

df2 = get_data()
fig1 = pie_chart()
fig2 = word_cloud()
fig3 = timeline_chart()

# page config
# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

# title image
title_image = Image.open("/home/lewagonvaleria/code/mfcorredor/DeepFeelings/DeepFeelings/images/deep-learning-large.jpg")
st.image(title_image)

#titles
st.markdown("""# DeepFeelings
## Brand Sentiment Analysis
""")
st.write("**Check out what people is thinking about your brand and products!**")
st.text_input('Insert the name of your brand')
st.text_input('Insert the name of your product')

# linecount
line_count = st.slider('Select a line count', 1, 10, 3)
head_df2 = df2.head(line_count)
head_df2


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
