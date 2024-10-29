import ast
import os
import pandas as pd

pathname = "./clean/output"
final_df = pd.DataFrame()


def blah(citation_counts):
    items = ast.literal_eval(citation_counts)
    for item in items:
        item_dict = dict(item)
        final_df[item_dict.get("year")] = item_dict.get("cited_by_count")


for filename in os.listdir(pathname):
    if os.path.isfile(os.path.join(pathname, filename)):
        df = pd.read_csv(os.path.join(pathname, filename), index_col=False)
        df.drop('authorships', axis=1, inplace=True)
        df.drop('ids', axis=1, inplace=True)
        df.drop('doi', axis=1, inplace=True)
        df.drop('topics', axis=1, inplace=True)
        df.drop('type', axis=1, inplace=True)
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df.drop('sustainable_development_goals', axis=1, inplace=True)
        final_df = pd.concat([final_df, df], ignore_index=True)
final_df.drop_duplicates(['id'], inplace=True)
final_df["counts_by_year"].apply(blah)
final_df.to_csv("./clean/done.csv", index=False)

