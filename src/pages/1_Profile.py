import os
import pandas as pd
import streamlit as st

from util.retrieve_probabilities import create_merge_probability_dict
from util.import_personas import read_personas

from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap

st.set_page_config(page_title="Personal Statistics", page_icon="🔎")

st.markdown("# Personal Stastics")

st.write(
    """This page aims to give insight in your clicking behaviour on this webapp based on personal statistics."""
)

cwd = os.getcwd()

# def read_personas(path_to_file: str = os.path.join(cwd, "src", "data", "persona.txt"))
#     personas = open(path_to_file, "r")
#     personas = personas.readlines()
#     personas = [x.rstrip() for x in personas]
#     return personas


# personas is structured as: ['Healthy Asian Food', 'American Meat Lover', 'Fat Craver', 'Green Health Freak']
personas = read_personas()

user_tracking_df = pd.read_csv(os.path.join(cwd, "src", "data", "user_clicking_history.csv"),
                               sep=";")
#user_tracking_df["timeplaceholder"] = [int(x[3:5]) for x in list(user_tracking_df["recipes"])]
user_tracking_df["timeplaceholder"] = [x[3:5] for x in list(user_tracking_df["recipes"])]


#calculate probabilities for the persona's
merged_probability_dict = create_merge_probability_dict(user_tracking_df)
merged_probability_dict = dict(sorted(merged_probability_dict.items()))

#personas = list(set(user_tracking_df['users']))
# personas = ["Green Health Freak", "Meat loving American",
#             "Healthy Asian", "Fat Craver"]
years = list(set(user_tracking_df['timeplaceholder']))
# Plotting the labels as ints causes an error in the web app
# they need to be ints to sort the list
years = [int(x) for x in years]
years.sort()
years = [str(x) for x in years]


green_health_freak = []
meat_loving_american = []
healthy_asian = []
fat_craver = []

for timeframe, prob_dict in merged_probability_dict.items():
    green_health_freak.append(prob_dict[personas[3]])
    meat_loving_american.append(prob_dict[personas[1]])
    healthy_asian.append(prob_dict[personas[0]])
    fat_craver.append(prob_dict[personas[2]])

#
data = {'personas': years,
        personas[3]: green_health_freak,
        personas[1]: meat_loving_american,
        personas[0]: healthy_asian,
        personas[2]: fat_craver}
prob_df = pd.DataFrame(data=data)
prob_df.to_csv(os.path.join(cwd, "src", "data", "user_persona_prob.csv"),
               sep=";", index=False)

palette = ["#c9d9d3", "#718dbf", "#e84d60", "#bfa271"]

#x = [ (persona, year) for persona in personas for year in years ]
x = [(year, persona) for year in years for persona in personas]

counts = sum(zip(data[personas[3]], data[personas[1]],
                 data[personas[0]], data[personas[2]]), ())  # like an hstack
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
