"""
# My first app
Here's our first attempt at using data to create a table:
"""

# multiple pages docs:
# https://docs.streamlit.io/library/get-started/multipage-apps/create-a-multipage-app
import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

from util.sample_rows_click_history import sample_rows

st.set_page_config(
    page_title="Recipes",
    page_icon="🌮",
)
user_name = "Daan"
st.sidebar.success("Select a demo above.")


def import_recipes(cwd: int = os.getcwd()):
    recipes_df = pd.read_csv(os.path.join(cwd, "src", "data", "recipes_small_labelled.csv"),
                             sep=";")
    recipes_name_img = recipes_df[["Name", "Images", "personas"]]
    recipes_name_img = recipes_name_img.dropna()
    return recipes_name_img


def clean_img_urls(list_of_urls):
    pattern = 'c\(\"(.*?)\.jpg'
    clean_urls = []
    for url in list_of_urls:
        m = re.search(pattern, url)
        if m:
            clean_url = m.group(1)
        else:
            clean_url = url
        clean_urls.append(clean_url)
    return clean_urls


# TO DO: meerdere images naast elkaar, referenties:
# https://discuss.streamlit.io/t/how-to-display-a-list-of-images-in-groups-of-10-50-100/32935/2
# https://discuss.streamlit.io/t/multiple-images-along-the-same-row/118/8
def show_recipes(input_dataframe: pd.DataFrame):
    # Create headers
    colms = st.columns((1, 2, 2, 2))
    fields = ["№", 'Recipe', 'Image', "action"]
    for col, field_name in zip(colms, fields):
        col.write(field_name)

    user_tracking_df = pd.read_csv(os.path.join(cwd, "src", "data", "user_clicking_history.csv"),
                               sep=";")

    # Fill the table
    for x, recipe_img_persona in enumerate(zip(list(input_dataframe["Name"]),
                          list(input_dataframe["Cleaned_images"]),
                          list(input_dataframe["personas"]))):
        col1, col2, col3, col4 = st.columns((1, 2, 2, 2))
        col1.write(x)  # index
        col2.write(recipe_img_persona[0])  # Name
        img_url = recipe_img_persona[1]
        img_url = re.sub('\"', '', img_url)
        col3.image(img_url)  # Image
        disable_status = recipe_img_persona[2]  # flexible type of button
        button_type = "Favorite" if disable_status else "Unfavorite"
        button_phold = col4.empty()  # create a placeholder
        do_action = button_phold.button(button_type, key=x)
        if do_action:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            cntr = len(user_tracking_df)
            user_tracking_df.loc[cntr] = [recipe_img_persona[2], current_time]
            cntr += 1
            user_tracking_df.to_csv(os.path.join(cwd, "src", "data", "user_clicking_history.csv"),
                                    sep=";", index=False)


# if a user tracking file exists, .. 
cwd = os.getcwd()
recipes_name_img = import_recipes()
clean_urls = clean_img_urls(recipes_name_img["Images"])
recipes_name_img["Cleaned_images"] = clean_urls
recipes_name_img = recipes_name_img.loc[recipes_name_img['Cleaned_images'] != "character(0)"]
prob_df = pd.read_csv(os.path.join(cwd, "src", "data", "user_persona_prob.csv"),
                      sep=";")
if os.path.isfile(os.path.join(os.getcwd(),
                               "src", "data", "user_persona_prob.csv")):
    sampled_df = sample_rows(prob_df, recipes_name_img)
    show_recipes(sampled_df)
else:
    show_recipes(recipes_name_img)
