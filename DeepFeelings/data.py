# import the mock data and select specific columns
import pandas as pd



def get_data():

    df2 = pd.read_csv('/home/lewagonvaleria/code/mfcorredor/DeepFeelings/raw_data/example_amz_rev.csv')
    df2 = df2[['texts', 'date','polarity']]
    #replace polarity numbers with words, sort date column date
    df2["polarity"].replace([2,1,0],['Positive','Neutral','Negative'], inplace=True)
    df2 = df2[['date','polarity']]
    df2.sort_values(by = ['date'], inplace=True)
    df2['date']= pd.to_datetime(df2['date'])

    return df2
