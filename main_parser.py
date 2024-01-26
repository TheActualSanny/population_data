from pydantic import BaseModel, field_validator, model_validator
import requests
import dotenv
import os
import csv
import json
import logging

dotenv.load_dotenv()

#setting up the logger for parsing.log
parsing = logging.getLogger('exception')
parsing.setLevel(logging.DEBUG)
format1 = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
file1 = logging.FileHandler('parsing.log')
file1.setFormatter(format1)
parsing.addHandler(file1)


#Initialized another logger for connection_statuses.log
conn = logging.getLogger('connection_report')
conn.setLevel(logging.INFO)
format2 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file2 = logging.FileHandler('connection_statuses.log')
file2.setFormatter(format2)
conn.addHandler(file2)


class Residental_Data(BaseModel):
    residental_area: str
    stated_year: int
    below_6: int
    from_6_to_10: int
    from_10_to_18: int
    from_18_to_25: int
    from_25_to_30: int
    from_30_to_50: int
    from_50_to_65: int
    from_65_to_75: int
    older_than_75: int
    
    @field_validator('from_10_to_18', 'from_6_to_10', 'from_10_to_18', 
                     'from_18_to_25', 'from_25_to_30', 'from_30_to_50',
                     'from_50_to_65', 'from_65_to_75', 'older_than_75',
                     'below_6', mode = 'before')
    @classmethod
    def check_below_6(cls, val):
        if val == '.' or not val:
            parsing.debug('Caught an exception! modified the value...')
            return 0
        else:
            return int(val)
        
    
url_csv = "https://opendata.duesseldorf.de/sites/default/files/Wohnbev%C3%B6lkerung%20nach%20Alter%20Wohnquartiere%20D%C3%BCsseldorf%202015_0.csv"
url_json_first = 'https://opendata.duesseldorf.de/api/action/datastore/search.json?resource_id=99ff11f6-ddfd-4698-86e9-453ce2ce859a'
url_json_second = "https://www.opendata.duesseldorf.de/api/action/datastore/search.json?resource_id=a9bb173d-8a0b-4d37-a6af-59ad1e9f485f"
# Will contain all of the instances of residental_data class and will be used in DB creation.
finalized_data = []

payload = {}
headers = {'User-Agent' : os.getenv('AGENT_DATA')}


response1 = requests.request("GET", url_csv, headers=headers, data=payload)
response2 = requests.request('GET', url_json_first, headers = headers, data = payload)
response3 = requests.request('GET', url_json_second, headers = headers, data = payload)

if not all([i == 200 for i in [response1.status_code, response2.status_code, response3.status_code]]):
    conn.error('Connection error occured. Make sure to provide the headers to the API...')
    raise ConnectionError('Connection error occured. Make sure to provide the headers to the API...')

else:
    conn.info('Connected to all 3 API-s successfully!')
    with open('2015_dusseldorf_data.csv', 'w') as f:
        f.write(response1.text)

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
                finalized_data.append(instance)

    for iter, data in enumerate([response2.text, response3.text], start = 1):
        json_data = json.loads(data)
        if iter == 1:
            upload_year = '2016'
        else:
            upload_year = '2017'     
        for record in json_data['result']['records']:
            values = list(record.values())
            if values.count('0') < 9:
                instance = Residental_Data(residental_area=values[0], stated_year=upload_year,
                                            from_6_to_10=values[2], from_10_to_18=values[3],
                                            from_18_to_25=values[4], from_25_to_30=values[5],
                                            from_30_to_50=values[6], from_50_to_65=values[7],
                                            from_65_to_75=values[8], older_than_75=values[9], 
                                            below_6=values[1])
                finalized_data.append(instance)

    if __name__ == '__main__':
        for instance in finalized_data:
            print(instance.residental_area, end = '\n')