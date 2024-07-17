import os.path
import pandas as pd
import json
import requests

import scope_file as project_scope

era = project_scope.era
institutions = project_scope.institution_list
nice_list = project_scope.NICE_LIST
file_name = 'test_csv.csv'
field_names = project_scope.data_fields


def query_year(my_year):
    global page_number, inst
    params = {
        'filter': f'publication_year:{str(my_year)},authorships.institutions.lineage:{"i865915315"},type:types/article',
        'select': 'id,ids,doi,topics,publication_year,fwci,type,cited_by_count,cited_by_percentile_year,'
                  'authorships,open_access,sustainable_development_goals,counts_by_year',
        'page': str(page_number),
        'mailto': str(nice_list)
    }
    api_url = "https://api.openalex.org/works"
    response = requests.get(api_url, params=params)
    return response.json()


def unpack(my_json, this_year):
    global file_name, keep_at_it, field_names

    file_name = str(".\\output\\") + str(this_year) + ".csv"
    keep_at_it = (int(my_json['meta']['page']) * int(my_json['meta']["per_page"]) < int(my_json['meta']['count']))

    for result in my_json["results"]:
        line_data = pd.Series()
        for key, val in field_names.items():
            try:
                print(field_names)
                print(f"key {key} \n")
                print(f"val {val} \n")
                line_data.loc[key] = result[val]
            except json.JSONDecodeError:
                line_data.loc[key] = "[]"
                continue
        if 'dataframe' not in globals():
            global dataframe
            dataframe = line_data.to_frame().T
        else:
            dataframe = pd.concat([dataframe, line_data.to_frame().T], ignore_index=True)
    if "dataframe" in globals():
        dataframe.to_csv(file_name, index=False, mode='a', header=not os.path.exists(file_name))
        del dataframe


for inst in institutions:
    for year in era:
        page_number = 1
        keep_at_it = True
        while keep_at_it:
            this_json = query_year(year)
            unpack(this_json, year)
            #  += 100 is obviously a test setting
            page_number += 100
            print(page_number)
