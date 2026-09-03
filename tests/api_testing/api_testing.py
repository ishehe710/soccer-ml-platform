import os
import requests
from dotenv import load_dotenv


# Load enviroment variables
load_dotenv()

# Example with Python

# testing Bzzoiro Sports API
API_KEY = os.getenv("SPORTS_BZZOIRO_API_KEY")
API_URL = f"{os.getenv("SPORTS_BZZOIRO_API_URL")}/api/v2/"


# inspecting premier and champions league
# - ids: Premier League = 1, Champions League = 7 
prem = 1
champs = 7
path = f'leagues/{prem}/season' 
headers = {"Authorization": f"Token {API_KEY}"}

print("premier league season 2026/27 available")
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

print("champions league season 2026/27 available")
path = f'leagues/{champs}/season' 
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

print("all available premier league seasons")
path = f'leagues/{prem}/seasons' 
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

print("all available champions league seasons")
path = f'leagues/{champs}/seasons' 
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

# teams
man_u = 17
psg = 114
path = f'teams/{man_u}'

print("man united data")
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

print("psg data")
path = f'teams/{psg}/squad'
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")


# matches
path = f'events/?league_id={prem}'
print("premier league matches")
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")


print("champions league matches")
path = f'events/?league_id={champs}'
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

# league standings
s_25_26 = 337

print("premier league standings")
path = f'leagues/{prem}/standings/?season_id={s_25_26}' 
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

print("champions league league standings")
path = f'leagues/{champs}/standings/?season_id={s_25_26}' 
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

# match stats
psg_ars = 206718

path = f'events/{psg_ars}/stats/'
print("psg vs arsenal")
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

mnu_liv = 351
path = f'events/{mnu_liv}/stats/'
print("man u vs liverpool")
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

# player stats
amad = 1792
path = f'players/{amad}/stats/'
print("amad diallo stats")
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")

dembouz = 1792
path = f'players/{dembouz}/stats/'
print("o. dembele stats")
r = requests.get(API_URL + path, headers=headers)
print(r.json())
print("\n------------------------------------------------------------------------\n")
