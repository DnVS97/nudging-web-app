import os
import pandas as pd


def f(x):
    if x == "Meat-loving American":
        x = "Meat loving American"
    return x


def sample_rows(probability_df: pd.DataFrame, recipes_df: pd.DataFrame,
                total_rows: int = 20):
    """Sample a number of rows based on the persona probability distribution.
    Given a total number of rows that are shown on the main page, we select
    (persona_prob * total_rows) rows from the dataframe to show on the main
    page. 

    Args:
        probability_df (pd.DataFrame): retrieved by the
        retrieve_probabilities.py script
        recipes_df (pd.DataFrame):
        total_rows (int, optional): Defaults to 20.

    Returns:
        _type_: A merged dataframe with samples from each persona
    """

    recipes_df["personas"] = recipes_df["personas"].apply(lambda x: f(x))

    last_row = probability_df.loc[[len(probability_df)-1]]
    col_names = list(last_row)[1:]

    list_of_dataframes = []
    for col_name in col_names:
        persona_prob = last_row[col_name].iloc[0]
        rows_to_sample = persona_prob * total_rows
        sliced_persona_df = recipes_df.loc[recipes_df["personas"] == col_name]
        sampled_df = sliced_persona_df.sample(n=round(rows_to_sample), replace=True)
        list_of_dataframes.append(sampled_df)
    complete_df = pd.concat(list_of_dataframes)
    return complete_df


if __name__ == "__main__":
    cwd = os.getcwd()
    prob_df = pd.read_csv(os.path.join(cwd, "src", "data", "user_persona_prob.csv"),
                          sep=";")

    recipes_df = pd.read_csv(os.path.join(cwd, "src", "data", "recipes_small_labelled.csv"),
                             sep=";")
    df = sample_rows(prob_df, recipes_df)
    print(df.head(5))