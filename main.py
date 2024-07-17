import os.path
import pandas as pd
import json
import requests

import scope_file as project_scope

era = project_scope.era
institutions = project_scope.institution_dict
nice_list = project_scope.NICE_LIST
file_name = 'test_csv.csv'
field_names = project_scope.data_fields
dataSet = []


def query_year(my_year, value):
    global page_number, inst, dataSet
    params = {
        'filter': f'publication_year:{str(my_year)},authorships.institutions.lineage:{value},type:types/article',
        'select': 'id,ids,doi,topics,publication_year,fwci,type,cited_by_count,cited_by_percentile_year,'
                  'authorships,open_access,sustainable_development_goals,counts_by_year',
        'page': str(page_number),
        'mailto': str(nice_list)
    }
    api_url = "https://api.openalex.org/works"
    response = requests.get(api_url, params=params)
    for resp in response.json()['results']:
        dataSet.append(resp)
    return response.json()['meta']


for key, value in institutions.items():
    for year in era:
        page_number = 1
        keep_at_it = True
        while keep_at_it:
            this_json = query_year(year, value)
            if int(this_json['page']) * int(this_json['per_page']) >= int(this_json['count']):
                keep_at_it = False
            page_number += 1
        datafile = pd.DataFrame.from_records(dataSet, exclude=['topics', 'authorships'])
        datafile.to_csv(".\\output\\" + str(key) + "_" + str(year) + ".csv")
        del dataSet
