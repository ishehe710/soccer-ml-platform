import os
import requests
from dotenv import load_dotenv

# Load enviroment variables
load_dotenv()

# Bzzoiro Sports API and authentication
API_KEY = os.getenv("SPORTS_BZZOIRO_API_KEY")
API_URL = f"{os.getenv("SPORTS_BZZOIRO_API_URL")}/api/v2/"
IMG_API_URL = f"{os.getenv("SPORTS_BZZOIRO_API_URL")}/img/"
headers = {"Authorization": f"Token {API_KEY}"}

# competition ids
prem = 1
champs = 7


def print_fetch_data(path, api_url,data_info):
    print(data_info)
    r = requests.get(api_url + path, headers=headers)
    print(r.json())
    print("\n------------------------------------------------------------------------\n")
    
    return r.json()

'''
    Extracting competition info from BZZoiro Sports API
'''
path = f"leagues"

##      EXTRACTION
# fetch
response = print_fetch_data(path, API_URL, "printing leagues endpoint") # competition info
print(type(response))


# finding appropriate leagues: Premier and Champions League
leagues_data = response['results']

prem_data = None
champs_data = None
for comp in leagues_data:
    if comp['id'] == prem:
        prem_data = comp
    if comp['id'] == champs:
        champs_data = comp
        


print("prem_data:", prem_data)
print("champs_data:", champs_data)

##      TRANSFORM
# make python schema of the postgres database

