import json
import requests
API_KEY = "AIzaSyBTQAbFNZRDdUv7FvKARgNtSgt4Vhx3qOs"

link = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" \
       "location=-33.8670522,151.1957362&" \
       "radius=500&" \
       "type=restaurant&" \
       "keyword=cruise&" \
       "key=AIzaSyBUx9LXpRH2sKejir6MHVTqRr_48GnUi1A"

def getNearestSearch(searchParams):
    link =  "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    r = requests.get(link, params = searchParams)
    print(r.url)
    return r.text

getNearestSearch({
    "location" : "50.450898"+","+"30.522719",
    "radius" : "50000",
    "key" : API_KEY
})
