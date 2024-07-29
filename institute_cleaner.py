import os
import ast
import pandas as pd

import scope_file as project_scope
uni_list = project_scope.institution_dict

path = './output'


def find_main_institute(json_string):
    collector = []
    for thingamadoodle in ast.literal_eval(json_string):
        match (thingamadoodle['id'].split("/"))[-1]:
            case "I865915315" | "I4210145651" | "I4210108594" | "I4210124285" | "I911458345" | "I4210153566":
                collector.append("Vrije Universiteit")
            case "I887064364" | "I4210145651" | "I4210109446" | "I4210108594" | "I4210114434" | "I4210153566" | "I2802928900":
                collector.append("Universiteit van Amsterdam")
            case "I121797337" | "I4210114434" | "I2800006345":
                collector.append("Universiteit Leiden")
            case "I913958620" | "I2801952686" | "I4210142620":
                collector.append("Erasmus Universiteit Rotterdam")
            case "I98358874" | "I4210145640" | "I4210099110":
                collector.append("Technische Universiteit Delft")
            case "I193700539" | "I124486421":
                collector.append("Universiteit van Tilburg")
            case "I83019370" | "I124486421":
                collector.append("Technische Universiteit Eindhoven")
            case "I34352273" | "I2801238018" | "I2800191616" | "I4210126394":
                collector.append("Universiteit Maastricht")
            case "i145872427" | "I2801238018" | "I4210126394" | "I2802934949":
                collector.append("Radboud Universiteit Nijmegen")
            case "I913481162":
                collector.append("Wageningen Universiteit")
            case "I193662353" | "I4210114434" | "I4210107283" | "I3018483916":
                collector.append("Universiteit Utrecht")
            case "I94624287" | "I4210122839":
                collector.append("Universiteit Twente")
            case "I169381384" | "I4210154073" | "I1334415907":
                collector.append("Rijksuniversiteit Groningen")
            case _:
                pass
    return set(collector)


for filename in os.listdir(path):
    f = os.path.join(path, filename)
    if os.path.isfile(f):
        df = pd.read_csv(f, index_col=False)
        df['authorships'] = df['authorships'].apply(find_main_institute)
        for key, value in uni_list.items():
            df[key] = df['authorships'].apply(lambda x: key in x)
        df.to_csv(".\\clean\\" + f, index=False)
