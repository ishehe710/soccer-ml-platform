'''

    Queries from the Sports Bzzoiro API, player info requsets
    and match info

'''
import os
import requests
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

def print_fetch_data(path, data_info):
    print(data_info)
    r = requests.get(API_URL + path, headers=headers)
    print(r.json())
    print("\n------------------------------------------------------------------------\n")

# Example with Python

# testing Bzzoiro Sports API
API_KEY = os.getenv("SPORTS_BZZOIRO_API_KEY")
API_URL = f"{os.getenv("SPORTS_BZZOIRO_API_URL")}/api/v2/"
AMAD = 1792

headers = {"Authorization": f"Token {API_KEY}"}

'''
PLayer info
'''


# players/id 
path = f'players/{AMAD}'
print("amad diallo info")
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")


# players/id/career
path = f'players/{AMAD}/career'
print("amad diallo career")
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

s_25_26 = 337
path = f'players/{AMAD}/stats/?season_id={s_25_26}'
print_fetch_data(path, "amad diallo 25/26 season stat logs per match")

'''
Match info
'''

# events/id
psg_ars = 206718
path = f'events/{psg_ars}'
print_fetch_data(path, 'psg vs arsenal match info')

# events/id/h2h
psg_ars = 206718
path = f'events/{psg_ars}/h2h'
print_fetch_data(path, 'psg vs arsenal head to head record')