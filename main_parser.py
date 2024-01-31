import requests
import dotenv
import os
import json
from residental_Data import Residental_Data
from logging_Setup import parsing
from csv_data import get_csv_Data
from json_data import get_json_Data

dotenv.load_dotenv()

payload = {}
headers = {'User-Agent' : os.getenv('AGENT_DATA')}
datasets = "https://data.europa.eu/api/hub/search/datasets/1a57a33d-3a99-4fbc-b56f-b4b109172c7d"
response = requests.request("GET", datasets, headers=headers, data=payload)
datasets_json = json.loads(response.text)
year_2015_url = datasets_json['result']['distributions'][0]['download_url']

url_csv = year_2015_url[0]
url_json_first = 'https://opendata.duesseldorf.de/api/action/datastore/search.json?resource_id=99ff11f6-ddfd-4698-86e9-453ce2ce859a'
url_json_second = "https://www.opendata.duesseldorf.de/api/action/datastore/search.json?resource_id=a9bb173d-8a0b-4d37-a6af-59ad1e9f485f"
# Will contain all of the instances of residental_data class and will be used in DB creation.
finalized_data = []


def main():
    global finalized_data
    finalized_data += get_csv_Data(url_csv) + get_json_Data(url_json_first, url_json_second)
    return finalized_data

call = main()


if __name__ == '__main__':
    for instance in finalized_data:
        print(instance.residental_area, end = '\n')
