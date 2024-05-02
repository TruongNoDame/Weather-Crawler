# Collecting Weather data using selenium on website

## Introduction
This is a project that collects data from websites using [Selenium](https://www.selenium.dev/) tool to automate the web browsing process, thereby automating the data collection process.

This project uses selenium to automate the web browsing process. However, during the implementation process, I realized that the ads in the [Meteostat website](https://meteostat.net/en/) can cause the automatic data collection process to be interrupted and cause errors. So, after doing some research, I used the AdBlock extension to block ads, thereby making the process of collecting fewer errors and easier.

## Usage
### 1. Check which provinces can collect data
Before starting I want you to read the meteostat_provinces.txt file. This is a file containing Vietnamese provinces that can collect weather data on the Meteosta website.

### 2. Running
To run the data collection code you need to run the following command:
```
python utils/meteostat_crawler.py --province_name="name of province" --days="number of days you want to collect"
```

After collecting the data, you will see that the column names are abbreviated and will be confusing. In addition, the data may have errors and may have Nah values ​​as well as date and time formats that may not be suitable for your purposes. So I suggest you run the code below:
```
python utils/preprocess_data.py --website_name="ex: meteostat.com" --decode_weather_code="True: Decode weather state or False: not decode weather state"
```

Note: you need to create a data directory including `data/meteostat/preprocessed` and `data/meteostat/un_preprocessed`
