import os
import pandas as pd

pathname = "./clean/output"
final_df = pd.DataFrame()

dir_path = ""
for folder in os.listdir(dir_path):
    folder_path = os.path.join(dir_path, folder)
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                df = pd.read_csv(os.path.join(folder_path, filename), index_col=0)
                df.drop('authorships', axis=1, inplace=True)
                df.drop('ids', axis=1, inplace=True)
                df.drop('doi', axis=1, inplace=True)
                df.drop('topics', axis=1, inplace=True)
                df.drop('type', axis=1, inplace=True)
                df.drop('Unnamed: 0', axis=1, inplace=True)
                df.drop('sustainable_development_goals', axis=1, inplace=True)
                final_df = final_df.append(df, ignore_index=True)
        final_df.drop_duplicates(['id'], inplace=True)
        final_df.to_csv(f"./clean/output/{filename.split('_')[0]}.csv", index=False)
        final_df = pd.DataFrame()

clean_df = pd.DataFrame()
for filename in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, filename)):
        df = pd.read_csv(os.path.join(dir_path, filename), index_col=0)
        clean_df.merge(df,
                       how='outer',
                       left_on=[
                           "id",
                           "publication_year",
                           "fwci",
                           "cited_by_count",
                           "cited_by_percentile_year",
                           "open_acces",
                           "counts_by_year"
                       ],
                       right_on=[])
