import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import emoji

#title
st.markdown("""# DeepFeelings
## Brand Sentiment Analysis
""")

#sidebar title
st.sidebar.write("**Check out what people is thinking about your brand and products!**")

# import the mock data and select specific columns
df2 = pd.read_csv('/home/lewagonvaleria/code/mfcorredor/DeepFeelings/raw_data/example_amz_rev.csv')
df2 = df2[['texts', 'date','polarity']]

#replace polarity numbers with words, sort date column date
df2["polarity"].replace([2,1,0],['Positive','Neutral','Negative'], inplace=True)
df2 = df2[['date','polarity']]
df2.sort_values(by = ['date'], inplace=True)
df2['date']= pd.to_datetime(df2['date'])

#calculate percentages of polarities for the pie chart
positive_percentage = int(21/50*100)
negative_percentage = int(16/50*100)
neutral_percentage = int(13/50*100)

# pie chart
labels = 'Positive', 'Negative', 'Neutral'
sizes = [42, 32, 26]
explode = (0.1, 0, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# line count (not very useful)
line_count = st.slider('Select a line count', 1, 10, 3)
head_df2 = df2.head(line_count)
head_df2

# buttons to dispay numbers (number of reviews, number of positive reviews, etc.)
st.button("Hola")

# pyploting piechart
st.pyplot(fig1)

# markdowns to add space
st.markdown("""
""")
st.markdown("""
""")


fig2, ax1 = plt.subplots()
#plt.figure(figsize=(12,5))
plt.hist(df2['polarity'], color='orange', width=0.7)


#timeline chart
df = pd.read_csv('/home/lewagonvaleria/code/mfcorredor/DeepFeelings/raw_data/example_amz_rev.csv').iloc[:,1:]
df['date'] = pd.to_datetime(df['date'])
df.sort_values(by = ['date'] , inplace = True)
df['polarity'] = df['polarity'].map({0:'negative',1:'neutral',2:'positive'})
df['year-month'] = df['date'].apply(lambda x : '-'.join(str(x).split('-')[:2]))
polarities_df = df.groupby('year-month').agg( polarity_fractions =
        ('polarity',
         lambda x : x.value_counts(normalize = True).to_dict()))
polars = ['negative','neutral','positive']

for polarity in polars:
    polarities_df.loc[:,polarity] = polarities_df['polarity_fractions']\
                                    .apply(lambda polarities_dict : polarities_dict.get(polarity))\
                                    .fillna(0.0)\
                                    .round(2)
polarities_df.drop( columns = ['polarity_fractions'] , inplace= True)
dummy = polarities_df.iloc[1,0]

import mplcyberpunk

polarity_colors = ['#850f2e','#bf810d','#0c853c']
plt.rcParams["font.family"] = "cursive"


polarity_emojis = [emoji.emojize('☹️') , emoji.emojize('😶') , emoji.emojize('😃')]

# places correctly the emojies on the rectangle
def get_index(idx, length):
    return  [idx < i*length for i in range(1,length)].index(True)

# for the background
with plt.style.context('cyberpunk'):
    fig , ax  = plt.subplots( nrows = 1 , ncols = 1)

    #plotting polarities timeline
    polarities_df.iloc[:10].plot(kind = 'bar' ,
                       width = 0.7 ,
                       figsize = (14,6),
                       color =  polarity_colors,
                       ax = ax);

    #storing coordinates for the line
    coords = []

    #placing emojies on the top of the rectangles
    for idx , patch in enumerate(ax.patches):

        #adding coordinates for the line
        xy_ = patch.get_x() + patch.get_width()/2 , patch.get_y() + patch.get_height()
        if idx >= len(ax.patches)*2/3:
            coords.append(xy_)


        #placing emojies
        ax.annotate( xy = (patch.get_x() + patch.get_width() / 12 , patch.get_y() + patch.get_height()),
                     text = polarity_emojis[get_index(idx , len(ax.patches)//3)],
                    fontsize = 20)

    #plotting line
    ax.plot(*zip(*coords) , color = 'pink')
    mplcyberpunk.make_lines_glow()

    ax.set_title("Polarity Timeline" , size = 25)
    ax.set_xlabel("Month" , size = 16)
    ax.set_ylabel("Polarities" , size = 16)
    ax.tick_params(axis = 'both' , which = 'major', labelsize = 14)
    ax.tick_params(axis = 'x' , which = 'major', rotation = 45 , labelsize = 14)

    #creating polarity box
    leg = ax.legend()
    leg = ax.legend(frameon=True ,
                    fancybox=True,
                    shadow=True ,
                    bbox_to_anchor=(1.11, 1.1),
                    prop={'size': 12},
                   title = "Polarity")

    #changing the size of the box titleÇ
    leg.get_title().set_size(14)

    #changing the border of the polarity box
    leg.get_frame().set_edgecolor('w')
    leg.get_frame().set_linewidth(0.1)


    plt.tight_layout()

st.pyplot(fig)

with st.sidebar:

    st.text_input('Brand')
    st.text_input('Product')
    st.pyplot(fig2)
