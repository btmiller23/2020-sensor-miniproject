#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime
import typing as T
import matplotlib.pyplot as plt
import numpy as np


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
    #starting to collect the data here
    #print(data)
    
    #temp median
    temp_data=pandas.DataFrame(data['temperature'])
    temp_data_median=temp_data.median()
    print('here are the temp medians',temp_data_median, sep='\n')
    #temp variance
    class1_temp_var=temp_data.class1.var()
    print('here is the class1 temp variance',temp_data.class1.var(),sep='\n')
    lab1_temp_var=temp_data.lab1.var()
    print('here is the lab1 temp variance',temp_data.lab1.var(),sep='\n')
    office_temp_var=temp_data.office.var()
    print('here is the office temp variance',temp_data.office.var(),sep='\n')
    
    #occupancy median
    occ_data=pandas.DataFrame(data['occupancy'])
    occ_data_median=occ_data.median()
    print('here are the occupancy medians',occ_data_median, sep='\n')
    #occupancy variance
    class1_occ_var=occ_data.class1.var()
    print('here is the class1 occupancy variance',class1_occ_var,sep='\n')
    lab1_occ_var=occ_data.lab1.var()
    print('here is the lab1 occupancy variance',lab1_occ_var,sep='\n')
    office_occ_var=occ_data.office.var()
    print('here is the office occupancy variance',office_occ_var,sep='\n')

    #PDF of sensor types
    co2_data=pandas.DataFrame(data['co2'])

    temp_PDF=temp_data.plot.kde()
    temp_PDF.set_title("Temperature Sensors PDF")
    temp_PDF.set_xlabel("Degrees Celcius")

    co2_PDF=co2_data.plot.kde()
    co2_PDF.set_title("co2 Sensors PDF")
    co2_PDF.set_xlabel("co2 Levels")
    
    occ_PDF=occ_data.plot.kde()
    occ_PDF.set_title("Occupancy Sensors PDF")
    occ_PDF.set_xlabel("Occupancy")
    
    #time interval stuff
    #following the method for temp occ and co2
    def datetime_to_float(d):
        return d.timestamp()

    time_interval={}
    for x in range(0,3102):
        time_interval[x]=datetime_to_float(occ_data.index[x+1])-datetime_to_float(occ_data.index[x])

    sensor_time={"sensor_time": pandas.DataFrame.from_dict(time_interval, "index").sort_index()}
    #now we get managable data
    time_interval_data=pandas.DataFrame(sensor_time['sensor_time'])
    #now use the data
    time_int_PDF=time_interval_data.plot.kde()
    time_int_PDF.set_title("Sensor Time Interval PDF")
    

    time_int_mean=time_interval_data.mean()
    print('here is the mean of the time intervals',time_int_mean,sep='\n')

    time_int_var=time_interval_data.var()
    print('here is the variance of the time intervals', time_int_var,sep='\n')

    for k in data:
        # data[k].plot()
        time = data[k].index
        data[k].hist()
        plt.figure()
        plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
        plt.xlabel("Time (seconds)")

    plt.show()
