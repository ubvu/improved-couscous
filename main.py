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

    api_url = ("https://api.openalex.org/works?page=" + str(page_number) +
               "&filter=authorships.institutions.lineage:i865915315,publication_year:" + str(my_year) + ","
               "type:types/article&select=id,topics,doi,ids,publication_year,fwci,type,cited_by_count,"
               "cited_by_percentile_year,open_access,sustainable_development_goals,counts_by_year"
               "&mailto=" + str(nice_list))
    response = requests.get(api_url)
    return response.json()


def unpack(my_json, this_year):
    global file_name, keep_at_it
    file_name = str(".\\output\\") + str(this_year) + ".csv"
    my_meta = pd.DataFrame.from_dict(pd.json_normalize(my_json['meta']))
    if int(my_meta['page'][0]) * int(my_meta["per_page"][0]) >= int(my_meta['count'][0]):
        keep_at_it = False
    my_data = my_json["results"]
    for result in my_data:
        global field_names
        for field_name in field_names:
            try:
                my_id = result[field_name]
                print(my_id)
                # now work on cleaning the data and save into file
            except Exception:
                continue

    # my_results = pd.DataFrame.from_dict(pd.json_normalize(my_json['results']), orient='columns')
    # my_results.to_csv(file_name, index=False, mode='a', header=not os.path.exists(file_name))


print(era)
for inst in institutions:
    for year in era:
        print(year)
        page_number = 1
        keep_at_it = True
        while keep_at_it:
            this_json = query_year(year)
            unpack(this_json, year)
            #  += 100 is obviously a test setting
            page_number += 100
            print(page_number)
