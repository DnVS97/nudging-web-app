import os
import pandas as pd
import random
random.randint(1, 2)

cwd = os.getcwd()

df = pd.read_csv(os.path.join(cwd, "src", "data", "recipes_small_labelled.csv"),
                 sep=";")
df_full = pd.read_csv(os.path.join(cwd, "src", "data", "recipes_small.csv"))

df["Images"] = df_full["Images"]

# add persona's 
persona_list = []
for sugar_label, diet_label, cuisine_label in zip(list(df['sugar_level']), list(df['Diet Label']), list(df['Cuisine Label'])):
    if diet_label == "Vegetarian" or diet_label == "Vegan":
        current_persona = "health freak"
    elif sugar_label == "high" and diet_label != "":
        current_persona = "sugar lover"
    elif diet_label == "Meat":
        current_persona = "meat lover"
    else:
        current_persona = "None"
    persona_list.append(current_persona)

df["personas"] = persona_list
df.to_csv(os.path.join(cwd, "src", "data", "recipes_small_labelled.csv"), 
                 sep=";", index=False)
