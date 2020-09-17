
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np

#First I'm making sure the file data is all here (same as analyze file)
def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data
    

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)

# Detect anomalies in temperature sensor data
temp_data=pandas.DataFrame(data['temperature'])

#I will use the "z score" method of finding outliers
anomalies={}

def anomaly_det(my_data):
    
    x=0
    #calculate the mean of the data set
    my_mean=np.mean(my_data)
    #find what one std is for the data
    one_std=np.std(my_data)

    #now we compare each data point to see if it is outside of 3 standard deviations
    for y in my_data:
        z_score= (y-my_mean)/one_std
        if np.abs(z_score) > 3:
            anomalies[x]=y
            x=x+1
    return anomalies

class1_anom=anomaly_det(temp_data.class1)
print('Out of ',len(temp_data.class1),'temp readings, there are ',len(class1_anom),' class 1 temp anomalies')


lab1_anom=anomaly_det(temp_data.lab1)
print('Out of ',len(temp_data.lab1),'temp readings, there are ',len(lab1_anom),' lab 1 temp anomalies')

office_anom=anomaly_det(temp_data.office)
print('Out of ',len(temp_data.office),'temp readings, there are ',len(office_anom),' office temp anomalies')

class1_temp_av=temp_data.class1.mean()
lab1_temp_av=temp_data.lab1.mean()
office_temp_av=temp_data.office.mean()

c1_std=np.std(temp_data.class1)
l1_std=np.std(temp_data.lab1)
o_std=np.std(temp_data.office)

c1_upper=class1_temp_av+(3*c1_std)
c1_lower=class1_temp_av-(3*c1_std)

l1_upper=lab1_temp_av+(3*l1_std)
l1_lower=lab1_temp_av-(3*l1_std)

o_upper=office_temp_av+(3*o_std)
o_lower=office_temp_av-(3*o_std)

print('The class 1 upper anomaly bound is ',c1_upper,' the lower bound is',c1_lower)
print('The lab 1 upper anomaly bound is ',l1_upper,' the lower bound is',l1_lower)
print('The office upper anomaly bound is ',o_upper,' the lower bound is',o_lower)



































