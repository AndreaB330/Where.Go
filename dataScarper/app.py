from pathlib import Path
import urllib.request
import webbrowser
import csv
import json
import time
import urllib
import requests
import os
from PIL import Image
from io import StringIO

API_KEY = "AIzaSyDuKTiibDg6ZWvUbLaSRMa2dJduPROIJXk"

log_file = open('log.txt', 'w')


def get_nearest_search(search_params):
    link = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    r = requests.get(link, params=search_params)
    return json.loads(r.text)


def genData():
    places = 0
    with open('places.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        places = list(reader)
    with open('result.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for place in places:
            res = get_place_details(place[0], place[1], place[2])
            if res != None:
                print("shta")
                link = requests.get("https://maps.googleapis.com/maps/api/place/photo",

                                    params={"photoreference": res['photos'][0]['photo_reference'],
                                            "key": "AIzaSyDNaQSqCab-57W17VcvxtgnMAcZKxIgnmg",
                                            "maxwidth": "500",
                                            "maxheight": "500"}).url

                writer.writerow([place[0], place[1], place[2], res['rating'], link])


def get_place_details(name, lat, lon):
    my_json = get_nearest_search({
        "location": lat + "," + lon,
        "radius": "1000",
        "key": "AIzaSyDNaQSqCab-57W17VcvxtgnMAcZKxIgnmg",
        "name": name
    })
    for place in my_json['results']:
        print(json.dumps(place, indent=4, sort_keys=True))
        print(place['name'])
        print(name)
        print("-" * 80)
        if not 'photos' in place:
            continue
        link = requests.head("https://maps.googleapis.com/maps/api/place/photo",
                             params={"photoreference": place['photos'][0]['photo_reference'],
                                     "key": "AIzaSyDNaQSqCab-57W17VcvxtgnMAcZKxIgnmg",
                                     "maxwidth": "200",
                                     "maxmaxheight": "200"
                                     })
        webbrowser.open_new_tab(link.url)
        s = input()
        if s != "":
            return place
    return None


def loadImages():
    counter = 0
    with open('result.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        places = list(reader)
        for place in places:
            counter += 1
            my_file = Path(str(counter)+".jpg")
            if my_file.is_file():
                continue

            print(place)
            urllib.request.urlretrieve(place[4], str(counter) + ".jpg")


if __name__ == '__main__':
    #genData()
    loadImages()