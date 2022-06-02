import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.markdown("""# DeepFeelings
## Brand Sentiment Analysis
Jannick, Lucía, María, Valeria""")

st.sidebar.write("Sidebar test")

df = pd.read_csv('/home/lewagonvaleria/code/mfcorredor/DeepFeelings/raw_data/twitter_training.csv', nrows= 100000)
df = df[df['Positive'] != 'Irrelevant']
df = df[['Positive', 'im getting on borderlands and i will murder you all ,' ]]
df.rename(columns = {'Positive' : 'Polarity', 'im getting on borderlands and i will murder you all ,' : 'Text'}, inplace = True)
positive_percentage = int(20831/61691*100)
negative_percentage = int(22542/61691*100)
neutral_percentage = int(18318/61691*100)
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Positive', 'Negative', 'Neutral'
sizes = [33, 36, 29]
explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')


fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider
line_count = st.slider('Select a line count', 1, 10, 3)

# and used in order to select the displayed lines
head_df = df.head(line_count)

head_df

labels = 'Positive', 'Negative', 'Neutral'
sizes = [33, 36, 29]
explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)

fig2, ax1 = plt.subplots()
#plt.figure(figsize=(12,5))
plt.hist(df['Polarity'], color='orange', width=0.7);

with st.sidebar:

    st.pyplot(fig2)
