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


st.set_page_config(
    page_title="Recipes",
    page_icon="🌮",
)
user_name = "Daan"
st.sidebar.success("Select a demo above.")


# import recipes dataframe
cwd = os.getcwd()
recipes_df = pd.read_csv(os.path.join(cwd, "src", "data", "recipes_small_labelled.csv"),
                         sep=";")

recipes_name_img = recipes_df[["Name", "Images", "personas"]]
#recipes_name_img = recipes_name_img[0:10]



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


clean_urls = clean_img_urls(recipes_name_img["Images"])
recipes_name_img["Cleaned_images"] = clean_urls
# only select the rows with an image
recipes_name_img = recipes_name_img.loc[recipes_name_img['Cleaned_images'] != "character(0)"]


# # Show user table 
colms = st.columns((1, 2, 2, 2))
fields = ["№", 'Recipe', 'Image', "action"]

for col, field_name in zip(colms, fields):
    # header
    col.write(field_name)

# import user tracking .csv
user_tracking_df = pd.read_csv(os.path.join(cwd, "src", "data", "user_clicking_history.csv"),
                               sep=";")


recipes_name_img = recipes_name_img[0:10]

# How to add images to a table:
# https://discuss.streamlit.io/t/table-of-media-pictures-or-audio/6925
# How to add clickable buttons in a table:
# https://discuss.streamlit.io/t/make-streamlit-table-results-hyperlinks-or-add-radio-buttons-to-table/7883/3
for x, recipe_img_persona in enumerate(zip(list(recipes_name_img["Name"]),
                          list(recipes_name_img["Cleaned_images"]),
                          list(recipes_name_img["personas"]))):
    #col1, col2, col3, col4, col5 = st.columns((1, 2, 2, 1, 1))
    col1, col2, col3, col4 = st.columns((1, 2, 2, 2))
    col1.write(x)  # index
    col2.write(recipe_img_persona[0])  # Name
    img_url = recipe_img_persona[1]
    img_url = re.sub('\"', '', img_url)
    col3.image(img_url)  # Image
    #col3.write(recipe_img_persona[1])  # Image
    #col3.write(st.image(recipe_img_persona[1]))  # Image
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

user_tracking_df
