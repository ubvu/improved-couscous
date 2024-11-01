import requests
import pandas as pd

import attention_list as api_targets


def add_mentions(my_json):
    global mentions
    for data in my_json:
        try:
            doi = data['attributes']['identifiers']['dois']
        except KeyError:
            doi = None
        try:
            msm = data['attributes']['mentions']['msm']
        except KeyError:
            msm = None
        try:
            policy = data['attributes']['mentions']['policy']
        except KeyError:
            policy = None
        new_df = {'doi': doi, 'msm': msm, 'policy': policy}
        mentions.append(new_df)


mentions = []
targets = api_targets.LINK_LIST
for target in targets:
    response = requests.get(target)
    response_data = response.json()
    add_mentions(response_data['data'])
    try:
        next_link = response_data['links']['next']
    except KeyError:
        next_link = None

    while next_link is not None:
        response = requests.get(next_link)
        response_data = response.json()
        add_mentions(response_data['data'])
        try:
            next_link = response_data['links']['next']
        except KeyError:
            next_link = None

pd.DataFrame.from_records(mentions).to_csv('./mentions/mentions.csv')
