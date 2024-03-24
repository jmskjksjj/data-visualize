import environ

# pip install python-environ
env = environ.Env()
env.read_env()
api_key = env("GOOGLE_API_KEY")

import googlemaps

gmaps = googlemaps.Client(key=api_key)
tmp = gmaps.geocode("서울영등포경찰서", language="ko")
tmp[0]["formatted_address"].split()[2]
tmp
