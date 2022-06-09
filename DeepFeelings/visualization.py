import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import emoji
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import mplcyberpunk
import plotly.graph_objects as go


def pie_chart(data):
    '''returns a piechart with percentage of negative, poistive and neutral reviews'''

    #calculate percentages of sentiment for the piechart
    total_rows = data.shape[0]

    positive_percentage = int(data['sentiment'].value_counts()['Positive']/total_rows*100)
    negative_percentage = int(data['sentiment'].value_counts()['Negative']/total_rows*100)
    neutral_percentage = int(data['sentiment'].value_counts()['Neutral']/total_rows*100)

    labels = ['Negative', 'Neutral', 'Positive']
    sizes = [negative_percentage, neutral_percentage, positive_percentage]
    #sentiment_colors = ['#850f2e','#bf810d','#0c853c']
    sentiment_colors = ['#E0427C', '#F0CA47', '#3CD3A9']

    #apply cyberpunk style
    with plt.style.context('cyberpunk'):
        #explode = (0.1, 0, 0)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            colors = sentiment_colors ,
            shadow=False, startangle=90, radius=1, frame=False, textprops={'fontsize': 8})

        #draw circle
        centre_circle = plt.Circle((0,0),0.70,fc='#212946')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        ax1.axis('equal')
        plt.title("Percentage of emotions in comments")

    return fig1

def word_cloud(string_of_words): #add topic as param
    ''' returns a word cloud from a list of words'''

    with plt.style.context('cyberpunk'):
        fig2 , ax1 = plt.subplots()
        wordcloud = WordCloud().generate(string_of_words)

        ax1.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        return fig2

def timeline_chart(data):
    '''returns a timeline chart of postive, negative and neutral rivews per month'''

    #importing the dataframe
    data["sentiment"] = data["sentiment"].apply(lambda x : x.capitalize())
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by = ['date'] , inplace = True)
    data['year-month'] = data['date'].apply(lambda x : '-'.join(str(x).split('-')[:2]))
    sentiment_data = data.groupby('year-month').agg( sentiment_fractions =
            ('sentiment',
            lambda x : x.value_counts(normalize = True).to_dict()))
    polars = ['Negative','Neutral','Positive']

    for sentiment in polars:
        sentiment_data.loc[:,sentiment] = sentiment_data['sentiment_fractions']\
                                        .apply(lambda sentiment_dict : sentiment_dict.get(sentiment))\
                                        .fillna(0.0)\
                                        .round(2)
    sentiment_data.drop( columns = ['sentiment_fractions'] , inplace= True)
    #dummy = sentiment_data.iloc[1,0]


    #sentiment_colors = ['#850f2e','#bf810d','#0c853c']
    sentiment_colors = ['#E0427C', '#F0CA47', '#3CD3A9']
    plt.rcParams["font.family"] = "cursive"


    sentiment_emojis = [emoji.emojize('☹️') , emoji.emojize('😶') , emoji.emojize('😃')]

    # places correctly the emojies on the rectangle
    def get_index(idx, length):
        return  [idx < i*length for i in range(1,length)].index(True)

    # for the background
    with plt.style.context('cyberpunk'):
        fig3 , ax  = plt.subplots( nrows = 1 , ncols = 1)

        #plotting sentiment timeline
        sentiment_data.iloc[:10].plot(kind = 'bar' ,
                        width = 0.7 ,
                        figsize = (14,6),
                        ax = ax ,
                        color =  sentiment_colors); # color can be added :

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
                        text = sentiment_emojis[get_index(idx , len(ax.patches)//3)],
                        fontsize = 20)

        #plotting line
        ax.plot(*zip(*coords) , color = 'pink')
        mplcyberpunk.make_lines_glow()

        ax.set_title("Sentiment Timeline" , size = 25)
        ax.set_xlabel("Month" , size = 16)
        ax.set_ylabel("Sentiment" , size = 16)
        ax.tick_params(axis = 'both' , which = 'major', labelsize = 14)
        ax.tick_params(axis = 'x' , which = 'major', rotation = 45 , labelsize = 14)

        #creating sentiment box
        leg = ax.legend()
        leg = ax.legend(frameon=True ,
                        fancybox=True,
                        shadow=True ,
                        bbox_to_anchor=(1.11, 1.1),
                        prop={'size': 12},
                    title = "Sentiment")

        #changing the size of the box title
        leg.get_title().set_size(14)

        #changing the border of the sentiment box
        leg.get_frame().set_edgecolor('w')
        leg.get_frame().set_linewidth(0.1)


        plt.tight_layout()

        return fig3


def timeline_chart_week(data):
    data["sentiment"] = data["sentiment"].apply(lambda x : x.capitalize())
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by = ['date'] , inplace = True)
    data['day'] = pd.to_datetime(data['date'].apply(lambda x : str(x).split(' ')[0]))
    sentiment_data = data.groupby('day').agg( sentiment_fractions =
                ('sentiment',
                lambda x : x.value_counts().to_dict()))
    polars = ['Negative','Neutral','Positive']

    for sentiment in polars:
        sentiment_data.loc[:,sentiment] = sentiment_data['sentiment_fractions']\
                                            .apply(lambda sentiment_dict : sentiment_dict.get(sentiment))\
                                            .fillna(0.0)\
                                            .round(2)
    sentiment_data.drop( columns = ['sentiment_fractions'] , inplace= True)


    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sentiment_data.index,
        y=sentiment_data.loc[:,"Negative"],
        name='Negative Comments',
        marker_color='#E0427C'
    ))
    fig.add_trace(go.Bar(
        x=sentiment_data.index,
        y=sentiment_data.loc[:,"Neutral"],
        name='Neutral Comments',
        marker_color='#F0CA47'
    ))

    fig.add_trace(go.Bar(
        x=sentiment_data.index,
        y=sentiment_data.loc[:,"Positive"],
        name='Positive Comments',
        marker_color='#3CD3A9'
    ))

    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(
         autosize=False,
         width=1400,
         height=600,
         paper_bgcolor="white",
        xaxis_tickangle = - 45,
        title='Social Media Activity',
        xaxis = dict(title = "Date" ,
                    tickfont_size=14),
        yaxis=dict(
            title='Number of Comments',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )

    return fig
