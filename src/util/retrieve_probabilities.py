import pandas as pd
import os


def retrieve_probability_dict(df):
    freq_dict = {}
    # count freqs
    for x in list(df["users"]):
        if not x in freq_dict:
            freq_dict[x] = 1
        else:
            freq_dict[x] += 1

    prob_dict = {}
    for persona, frequency in freq_dict.items():
        prob = frequency / len(df)
        prob_dict[persona] = prob
    
    # add the persona's that are not found 
    personas = ["Green Health Freak", "American Meat-Lover", "Healthy Asian", "Fat Craver"]
    for persona in personas:
        if persona not in list(prob_dict.keys()):
            prob_dict[persona] = 0.0
    return prob_dict


def create_merge_probability_dict(df):
    merged_prob_dict = {}
    for x in list(set(df["timeplaceholder"])):
        sliced_df = df.loc[df['timeplaceholder'] == x]
        probability_dict = retrieve_probability_dict(sliced_df)
        merged_prob_dict[x] = probability_dict
    return merged_prob_dict


if __name__ == "__main__":
    cwd = os.getcwd()
    user_tracking_df = pd.read_csv(os.path.join(cwd, "src", "data", "user_clicking_history.csv"),
                               sep=";")
    user_tracking_df["timeplaceholder"] = [x[3:5] for x in list(user_tracking_df["recipes"])]
    merged_probability_dict = create_merge_probability_dict(user_tracking_df)
    










# fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
# years = ['2015', '2016', '2017']

# data = {'fruits' : fruits,
#         '2015'   : [2, 1, 4, 3, 2, 4],
#         '2016'   : [5, 3, 3, 2, 4, 6],
#         '2017'   : [3, 2, 4, 4, 5, 3]}

# palette = ["#c9d9d3", "#718dbf", "#e84d60"]

# # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
# x = [ (fruit, year) for fruit in fruits for year in years ]
# counts = sum(zip(data['2015'], data['2016'], data['2017']), ()) # like an hstack

# source = ColumnDataSource(data=dict(x=x, counts=counts))

# p = figure(x_range=FactorRange(*x), height=350, title="Fruit Counts by Year",
#            toolbar_location=None, tools="")

# p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
#        fill_color=factor_cmap('x', palette=palette, factors=years, start=1, end=2))

# p.y_range.start = 0
# p.x_range.range_padding = 0.1
# p.xaxis.major_label_orientation = 1
# p.xgrid.grid_line_color = None

# #show(p)
# st.bokeh_chart(p, use_container_width=True)