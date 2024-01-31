from logging_Setup import parsing
from residental_Data import Residental_Data
import csv
import requests

def get_csv_Data(url = None):
    if not url:
        raise ValueError('Provide an URL!')
    
    response = requests.request('GET', url = url)
    csv_Data = []

    with open('2015_dusseldorf_data.csv', 'w') as f:
        f.write(response.text)
    
    with open('2015_dusseldorf_data.csv', 'r') as f:
        csv_reader = csv.DictReader(f, delimiter = ';')
        for residental_area in csv_reader:
            values = list(residental_area.values())
            if values.count('0') < 9:
                instance = Residental_Data(residental_area=values[0], stated_year=f.name[0:4],
                                        from_6_to_10=values[2], from_10_to_18=values[3],
                                        from_18_to_25=values[4], from_25_to_30=values[5],
                                        from_30_to_50=values[6], from_50_to_65=values[7],
                                        from_65_to_75=values[8], older_than_75=values[9], 
                                        below_6=values[1])
                csv_Data.append(instance)
    parsing.info('Finished CSV parsing successfully!')
    return csv_Data
