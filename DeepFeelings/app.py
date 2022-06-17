import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import emoji
import plotly.express as px
from PIL import Image
from visualization import pie_chart, timeline_chart, word_cloud, timeline_chart_week
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


class Pagination:

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

    """

    def __init__(self):
        if "runpage" not in st.session_state:
            st.session_state.runpage = self.main_page
            self.topics = None
        st.session_state.runpage()

    def main_page(self):
        set_bg_hack('../background_opt.gif')
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
        st.write(f'<style>{Pagination.CSS}</style>', unsafe_allow_html=True)
        if st.button("Get report"):
            st.session_state["brand"] = brand
            st.session_state["product"] = product
            st.session_state.runpage = self.second_page
            st.session_state.runpage()
            st.experimental_rerun()

    def second_page(self):
        #set_bg_hack('bg_neurons.webp')
        st.markdown("""<p style="font-family:sans-serif; font-weight:bold; color:White; font-size: 40px;">
                        DeepFeelings</p>""", unsafe_allow_html = True)

        representation = f"Sentiment Analysis for {st.session_state['product']}."
        if st.session_state["brand"]:
            representation = representation[:-1] + f" ({st.session_state['brand']})."
        st.markdown(f"""<p style="font-family:sans-serif; font-weight:bold; color:White; font-size: 40px;">
                        {representation}</p>""", unsafe_allow_html = True)

        self.topics = pd.read_csv('../raw_data/topics_neg.csv', index_col='brand_product')
        brand = st.session_state["brand"]
        product = st.session_state["product"]
        brand = brand.lower()
        product = product.lower()
        if brand != '' and product != '':
            file_list = [f"../raw_data/sentiment_amz_{product}.csv",
                         f"../raw_data/sentiment_tw_{brand}.csv"]
            csv_list = [pd.read_csv(file) for file in file_list]
            data = pd.concat(csv_list, ignore_index=True)
            data_amz = pd.read_csv(file_list[0])
            data_amz['date'] = pd.to_datetime(data['date'])
            topic = self.topics['negative_topics'][brand]
            fig3 = timeline_chart(data_amz)
        elif brand != '':
            data = pd.read_csv(f"../raw_data/sentiment_tw_{brand}.csv")
            fig4 = timeline_chart_week(data)
            topic = self.topics['negative_topics'][f"{brand}_tw"]
        elif product != '':
            data = pd.read_csv(f"../raw_data/sentiment_amz_{product}.csv")
            data['date'] = pd.to_datetime(data['date'])
            topic = self.topics['negative_topics'][f"{product}_amz"]
            fig3 = timeline_chart(data)


        fig1 = pie_chart(data)
        fig2 = word_cloud(topic)

        # linecount
        # line_count = st.slider('Select a line count', 1, 10, 3)
        # head_data = data.head(line_count)
        # head_data
        # st.dataframe(head_data)

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
            st.markdown("""<p style="font-family:sans-serif; font-weight:bold; color:White; font-size: 30px;">
                        Keywords of negative comments</p>""",
                        unsafe_allow_html=True)
            second_column = columns[1].pyplot(fig2)
        if product != '':
            st.pyplot(fig3)

        if brand != '':
            st.plotly_chart(fig4)


        st.write(f'<style>{Pagination.CSS}</style>', unsafe_allow_html=True)
        if st.button("Return to main"):
            st.session_state.runpage = self.main_page
            st.session_state.runpage()
            st.experimental_rerun()


if __name__ == "__main__": Pagination()
