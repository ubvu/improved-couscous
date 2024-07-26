import os
import ast
import pandas as pd

path = './output'


def find_main_institute(json_string):
    collector = []
    for thingamadoodle in ast.literal_eval(json_string):
        match (thingamadoodle['id'].split("/"))[-1]:
            case "I865915315" | "I4210145651" | "I4210108594" | "I4210124285" | "I911458345" | "I4210153566":
                collector.append("vrije universiteit")
            case "I887064364" | "I4210145651" | "I4210109446" | "I4210108594" | "I4210114434" | "I4210153566" | "I2802928900":
                collector.append("universiteit van amsterdam")
            case "I121797337" | "I4210114434" | "I2800006345":
                collector.append("universiteit leiden")
            case "I913958620" | "I2801952686" | "I4210142620":
                collector.append("erasmus universiteit rotterdam")
            case "I98358874" | "I4210145640" | "I4210099110":
                collector.append("technische universiteit delft")
            case "I193700539" | "I124486421":
                collector.append("tilburg universiteit")
            case "I83019370" | "I124486421":
                collector.append("technische universiteit eindhoven")
            case "I34352273" | "I2801238018" | "I2800191616" | "I4210126394":
                collector.append("universiteit maastricht")
            case "i145872427" | "I2801238018" | "I4210126394" | "I2802934949":
                collector.append("radboud universiteit nijmegen")
            case "I913481162":
                collector.append("wageningen universiteit")
            case "I193662353" | "I4210114434" | "I4210107283" | "I3018483916":
                collector.append("universiteit utrecht")
            case "I94624287" | "I4210122839":
                collector.append("universiteit twente")
            case "I169381384" | "I4210154073" | "I1334415907":
                collector.append("rijksuniversiteit groningen")
            case _:
                pass
    return set(collector)


for filename in os.listdir(path):
    f = os.path.join(path, filename)
    if os.path.isfile(f):
        df = pd.read_csv(f)
        df['authorships'] = df['authorships'].apply(find_main_institute)
        df.to_csv(".\\clean\\" + f)
