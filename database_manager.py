from main_parser import finalized_data
import mysql.connector
import os
import dotenv
import logging

logg = logging.getLogger('database_exceptions')
logg.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file = logging.FileHandler('database_exceptions.log')
file.setFormatter(formatter)
logg.addHandler(file)

dotenv.load_dotenv()

conn = mysql.connector.connect(
    host = os.getenv('HOST'),
    user = os.getenv('USER'),
    password = os.getenv('PASS'),
    database = os.getenv('DB')
)

cursor = conn.cursor()

index = 1
cursor.execute('CREATE DATABASE IF NOT EXISTS citizen_data')

cursor.execute("""CREATE TABLE IF NOT EXISTS dusseldorf_data(
            id integer PRIMARY KEY,
            residental_area text,
            year integer,
            below_6 integer,
            from_six_to_10 integer,
            from_ten_to_18 integer,
            from_eighteen_to_25 integer,
            from_twentyfive_to_30 integer,
            from_thirty_to_50 integer,
            from_fifty_to_65 integer,
            from_sixtyfive_to_75 integer,
            older_than_75 integer
)""")

def find_Resident_Area(resident_area):
    cursor.execute('SELECT * FROM dusseldorf_data WHERE residental_area = %s', (resident_area,))
    data = cursor.fetchall()
    if not data:
        logg.info('Failed to find the given residental area...')
    return data


def delete_Residental_Area(resident_area):
    if find_Resident_Area(resident_area):
        cursor.execute('DELETE FROM dusseldorf_data WHERE residental_area = %s', (resident_area,))
    else:
        logg.info('Failed to delete the given residental area...')

# for instance in finalized_data:
#     cursor.execute('''INSERT INTO dusseldorf_data (id, residental_area, year, below_6, from_six_to_10,
#                     from_ten_to_18, from_eighteen_to_25, from_twentyfive_to_30, from_thirty_to_50, from_fifty_to_65,
#                     from_sixtyfive_to_75, older_than_75) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (index, instance.residental_area, instance.stated_year, instance.below_6,
#                                                                                                                       instance.from_6_to_10, instance.from_10_to_18, instance.from_18_to_25, instance.from_25_to_30,
#                                                                                                                       instance.from_30_to_50, instance.from_50_to_65, instance.from_65_to_75, instance.older_than_75))
#     index += 1


conn.commit()
cursor.close()
conn.close()
