# radboud university is a mess because they don't separate their UMC,
# so we will try and clean it up with openaire.

import time
import json
import pandas as pd
import requests

import attention_list as api_targets

access_token = ""
page = 1
df = pd.DataFrame()
dothis = True


def make_access_token():
    global access_token
    url = api_targets.OPENAIRE_REFRESHER + api_targets.OPENAIRE_RT
    print(url, "\n")
    response = requests.get(url, headers={"accept": "application/json"})
    my_data = response.json()
    access_token = my_data['access_token']
    print(access_token)


def api_call(my_year):
    global access_token, page
    # params = {
    #     "search": "OpenAIRE Graph",
    #     "type": "publication",
    #     "fromPublicationDate": str(my_year) + "01-01",
    #     "toPublicationDate": str(my_year) + "-12-31",
    #    "relOrganizationId": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    #     "pageSize": "100",
    #     "page": str(page)
    # }
    params = {
        "search": "OpenAIRE Graph",
        "type": "publication",
        "fromPublicationDate": str(my_year) + "-01-01",
        "toPublicationDate": str(my_year) + "-12-31",
        "relCollectedFromDatasourceId": "opendoar____%253A%253A7bccfde7714a1ebadf06c5f4cea752c1",
        "pageSize": "100",
        "page": str(page)
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + access_token
    }
    url = api_targets.OPENAIRE_ENDPOINT
    response = requests.get(url, params=params, headers=headers)
    my_data = response.json()
    print(json.dumps(my_data, indent=4, sort_keys=True))
    return my_data


def unpack(my_data):
    global dothis, page, df
    page = int(my_data['header']['page'])
    size = int(my_data['header']['pageSize'])
    total = int(my_data['header']['numFound'])
    if page > total // size:
        dothis = False
    else:
        page += 1
    if my_data['results']:
        df = df.append(my_data.results, ignore_index=True)
    print(dothis)


make_access_token()
for year in range(2016, 2024):
    dothis = True
    while dothis:
        data = api_call(year)
        unpack(data)
        time.sleep(5)
df.to_csv("./openaire_output/radboud.csv", index=False)






