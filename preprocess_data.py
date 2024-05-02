import pandas as pd
import os
from datetime import datetime
import argparse
import re
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--website_name', type=str, required=True)
parser.add_argument('--decode_weather_code', type=str, default='False', required=False)
args = parser.parse_args()

website_name = args.website_name.split('.')[0].lower()
print('Website:',website_name)
decode_weather_code = str(args.decode_weather_code).lower() == "true"
print('Decode weather code:',decode_weather_code)
dir_path = os.path.join(os.getcwd(),'data',f'{website_name}')
un_preprocessed_dir_path = os.path.join(dir_path,'un_preprocessed')
preprocessed_dir_path = os.path.join(dir_path,'preprocessed')

def preprocess_meteostat(dir_path):
    weather_state = {
    0: 'Unknown',
    1: 'Clear',
    2: 'Fair',
    3: 'Cloudy',
    4: 'Overcast',
    5: 'Fog',
    6: 'Freezing Fog',
    7: 'Light Rain',
    8: 'Rain',
    9: 'Heavy Rain',
    10: 'Freezing Rain',
    11: 'Heavy Freezing Rain',
    12: 'Sleet',
    13: 'Heavy Sleet',
    14: 'Light Snowfall',
    15: 'Snowfall',
    16: 'Heavy Snowfall',
    17: 'Rain Shower',
    18: 'Heavy Rain Shower',
    19: 'Sleet Shower',
    20: 'Heavy Sleet Shower',
    21: 'Snow Shower',
    22: 'Heavy Snow Shower',
    23: 'Lightning',
    24: 'Hail',
    25: 'Thunderstorm',
    26: 'Heavy Thunderstorm',
    27: 'Storm',
    1000: 'Unknown'
    }

    for filename in os.listdir(dir_path):
        if filename.endswith(".csv"):
            try: 
                csv_file = os.path.join(dir_path, filename)
                me_data=pd.read_csv(csv_file)
                me_data = me_data.rename(columns={'time':'Time','temp':'Temp(C)', 'dwpt':'Dew_point(C)','rhum':'Humidity(%)', 'prcp':'Precipitation(mm)','snow':'Snow_Depth','wdir':'Wind_direct','wspd':'Wind_speed(km/h)','wpgt':'Peak_gust','pres':'Barometer(mbar)','tsun':'Sunshine_duration',	'coco':'Weather'})
                me_data['Time']=[datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')for date in me_data['Time']]
                me_data['Temp(C)'] = [float(temp) for temp in me_data['Temp(C)']]
                me_data['Weather'] = me_data['Weather'].fillna(1000).astype(int)
                me_data['Barometer(mbar)'] = me_data['Barometer(mbar)'].fillna(1100).astype(int)
                if decode_weather_code:
                    me_data['Weather'] = [weather_state[code] for code in me_data['Weather']]
                me_data.to_csv(os.path.join(preprocessed_dir_path,filename))
                print("Done")
            except Exception as err:
                print(f"{type(err).__name__} was raised {err}")#print the error
                print("Dataset is already preprocessed!")
    return


preprocess_meteostat(un_preprocessed_dir_path)