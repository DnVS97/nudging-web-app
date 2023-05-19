import os
import pandas as pd

cwd = os.getcwd()
recipes_df = pd.read_csv(os.path.join(cwd, "src", "data",
                                      "recipes_small_labelled.csv"), sep=";")
unique_personas = set(list(recipes_df["personas"]))
unique_personas = {x for x in unique_personas if x==x}

with open(os.path.join(cwd, "src", "data", "persona.txt"), "w") as f:
    for persona in unique_personas:
        f.write(f"{persona}\n")
