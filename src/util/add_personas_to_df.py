import os
import pandas as pd
import random


cwd = os.getcwd()



personas = read_personas()
df = pd.read_csv(os.path.join(cwd, "src", "data", "recipes_small_labelled.csv"),
                 sep=";")
df_full = pd.read_csv(os.path.join(cwd, "src", "data", "recipes_small_filt.csv"))

df['Price Label'] = ["High Price" if random.randint(1, 2) ==1 else "Low Price" for x in range(len(df))]

df["Images"] = df_full["Images"]

# add persona's 
persona_list = []
for diet_label, cuisine_label, health_label in zip(list(df['Diet Label']), list(df['Cuisine Label']), list(df['Fat Label'])):
    if diet_label == "Vegetarian" or diet_label == "Vegan" and health_label == "Low Fat":
        current_persona = personas[3]
    elif cuisine_label == "American" and  diet_label == "Meat" and health_label == "High Fat":
        current_persona = personas[1]
    elif cuisine_label == "Asian" and health_label == "Low Fat":
        current_persona = personas[0]
    elif health_label == "High Fat" and diet_label != "Vegan": 
        current_persona = personas[2]
    else:
        current_persona = "None"
    persona_list.append(current_persona)

df["personas"] = persona_list
df.to_csv(os.path.join(cwd, "src", "data", "recipes_small_labelled.csv"), 
                 sep=";", index=False) 
