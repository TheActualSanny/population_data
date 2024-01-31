import requests
import json
from logging_Setup import parsing
from residental_Data import Residental_Data



def get_json_Data(url = None, *urls):
    if not urls:
        raise ValueError('Provide an URL!')
    iter = 2015
    json_Data = []

    for index, url in enumerate(urls, start = 1):
        response = requests.request('GET', url = url)
        upload_year = iter + 1
        jsonn = json.loads(response.text)
     
        for record in jsonn['result']['records']:
            values = list(record.values())
            if values.count('0') < 9:
                instance = Residental_Data(residental_area=values[0], stated_year=upload_year,
                                            from_6_to_10=values[2], from_10_to_18=values[3],
                                            from_18_to_25=values[4], from_25_to_30=values[5],
                                            from_30_to_50=values[6], from_50_to_65=values[7],
                                            from_65_to_75=values[8], older_than_75=values[9], 
                                            below_6=values[1])
                json_Data.append(instance)
    parsing.info('Finished JSON parsing successfully!')
    return json_Data
