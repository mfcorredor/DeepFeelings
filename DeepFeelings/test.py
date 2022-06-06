import pandas as pd

from cluster_viz import get_clusters_plotted

df = pd.read_csv("../raw_data/testdata.manual.2009.06.14.csv")
get_clusters_plotted(df, plotting = True)
