import os
import pandas as pd
import streamlit as st

from util.retrieve_probabilities import create_merge_probability_dict

from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap

st.set_page_config(page_title="Personal Statistics", page_icon="🔎")

st.markdown("# Personal Stastics")
st.sidebar.header("Personal Stastics")

st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

cwd = os.getcwd()
user_tracking_df = pd.read_csv(os.path.join(cwd, "src", "data", "user_clicking_history.csv"),
                               sep=";")
user_tracking_df["timeplaceholder"] = [x[3:5] for x in list(user_tracking_df["recipes"])]


#calculate probabilities for the persona's
merged_probability_dict = create_merge_probability_dict(user_tracking_df)
merged_probability_dict = dict(sorted(merged_probability_dict.items()))

#personas = list(set(user_tracking_df['users']))
personas = ["Green Health Freak", "Meat loving American",
                "Healthy Asian", "Fat Craver"]
years = list(set(user_tracking_df['timeplaceholder']))


green_health_freak = []
meat_loving_american = []
healthy_asian = []
fat_craver = []

for timeframe, prob_dict in merged_probability_dict.items():
    green_health_freak.append(prob_dict["Green Health Freak"])
    meat_loving_american.append(prob_dict["Meat loving American"])
    healthy_asian.append(prob_dict["Healthy Asian"])
    fat_craver.append(prob_dict["Fat Craver"])

#
data = {'personas': years,
        'green_health_freak': green_health_freak,
        'meat_loving_american': meat_loving_american,
        'healthy_asian': healthy_asian,
        'fat_craver': fat_craver}


palette = ["#c9d9d3", "#718dbf", "#e84d60", "#e22d60"]
#palette = ["#c9d9d3", "#718dbf", "#e84d60"]

#x = [ (persona, year) for persona in personas for year in years ]
x = [(year, persona) for year in years for persona in personas]

counts = sum(zip(data['green_health_freak'], data['meat_loving_american'],
                 data['healthy_asian'], data['fat_craver']), ())  # like an hstack
#counts = sum(zip(data['11'], data['20'], data['35']), ()) # like an hstack


source = ColumnDataSource(data=dict(x=x, counts=counts))

p = figure(x_range=FactorRange(*x), height=350, title="Persona over time",
           toolbar_location=None, tools="")

p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
       fill_color=factor_cmap('x', palette=palette, factors=personas, start=1, end=2))

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None

#show(p)
st.bokeh_chart(p, use_container_width=True)
