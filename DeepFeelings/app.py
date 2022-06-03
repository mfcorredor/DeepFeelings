import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import emoji
import plotly.express as px
from data import get_data
from visualization import pie_chart, timeline_chart, bar_chart

df2 = get_data()
fig1 = pie_chart()
fig2 = bar_chart()
fig3 = timeline_chart()

# page config
# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

#title
st.markdown("""# DeepFeelings
## Brand Sentiment Analysis
""")
#sidebar title
with st.sidebar:
    st.sidebar.write("**Check out what people is thinking about your brand and products!**")
    st.text_input('Brand')
    st.text_input('Product')

# linecount
line_count = st.slider('Select a line count', 1, 10, 3)
head_df2 = df2.head(line_count)
head_df2

# buttons to dispay numbers (number of reviews, number of positive reviews, etc.)
st.button("Hola")

#columns creation
columns = st.columns(2)
first_column = columns[0].pyplot(fig1)

# markdowns to add space
st.markdown("""
""")
st.markdown("""
""")
second_column = columns[1].pyplot(fig2)

st.pyplot(fig3)
