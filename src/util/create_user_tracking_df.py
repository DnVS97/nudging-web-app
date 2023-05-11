import pandas as pd
import os

persona = []
timeframe = []
df = pd.DataFrame({"users": persona, "recipes": timeframe})
df.to_csv(os.path.join(os.getcwd(), "src", "data", "user_clicking_history.csv"),
          sep=";", index=False)
