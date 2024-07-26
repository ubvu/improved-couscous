import os.path
import pandas as pd
import json
import requests

import scope_file as project_scope

era = project_scope.era
institutions = project_scope.institution_dict
nice_list = project_scope.NICE_LIST


def query_year(my_year, my_value):
    global page_number, dataSet
    params = {
        'filter': f'publication_year:{str(my_year)},authorships.institutions.lineage:{my_value},type:types/article',
        'select': 'id,ids,doi,topics,publication_year,fwci,type,cited_by_count,cited_by_percentile_year,'
                  'authorships,open_access,sustainable_development_goals,counts_by_year',
        'page': str(page_number),
        'mailto': str(nice_list)
    }
    api_url = "https://api.openalex.org/works"
    response = requests.get(api_url, params=params)
    for resp in response.json()['results']:
        resp2 = {}
        for key1, value1 in resp.items():
            if key1 == "topics":
                topics = {}
                for val in value1:
                    if float(val["score"]) >= 0.8:
                        topics.update({"id": val["id"], "display_name": val["display_name"],
                                       "field": val["field"]["display_name"], "score": val["score"]})
                    else:
                        break
                resp2.update({key1: topics})
            elif key1 == "authorships":
                authorships = []
                for val in value1:
                    for inst in val["institutions"]:
                        authorships.append({"id": inst["id"], "display_name": inst["display_name"]})
                resp2.update({key1: authorships})
            else:
                resp2.update({key1: value1})
        dataSet.append(resp2)
        del resp2
    return response.json()['meta']


for key, value in institutions.items():
    for year in era:
        dataSet = []
        page_number = 1
        keep_at_it = True
        while keep_at_it:
            this_json = query_year(year, value)
            if int(this_json['page']) * int(this_json['per_page']) >= int(this_json['count']):
                keep_at_it = False
            page_number += 1
        datafile = pd.DataFrame.from_records(dataSet)
        datafile.to_csv(".\\output\\" + str(key) + "_" + str(year) + ".csv")
        del dataSet
