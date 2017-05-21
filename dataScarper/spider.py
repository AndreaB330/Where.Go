import json
import time
import requests
import os

API_KEY = "AIzaSyDuKTiibDg6ZWvUbLaSRMa2dJduPROIJXk"

Kyiv = "50.4496098,30.5210332"
London = "51.5073689,-0.1278953"
log_file = open('log.txt', 'w')

def log(*params, **keys):
    print(*params, **keys)
    print(*params, **keys, file=log_file)


def get_radar_search(search_params):
    link = "https://maps.googleapis.com/maps/api/place/radarsearch/json"
    r = requests.get(link, params=search_params)
    return json.loads(r.text)


def get_place_details(search_params):
    link = "https://maps.googleapis.com/maps/api/place/details/json"
    r = requests.get(link, params=search_params)
    return json.loads(r.text)


def create_detail_files(radar_search_file_name, directory):
    place_list = json.loads(open(directory + '\\' + radar_search_file_name + '.json').read())
    directory += '\\place_details'
    if not os.path.exists(directory):
        os.makedirs(directory)

    counter = 0
    time_sum = 0
    if len(place_list['results']) == 0:
        return
    for place in place_list['results']:
        time_start = time.time()

        f = open(directory + '\\' + place['place_id'] + '.json', 'w')

        my_json = get_place_details({
            "placeid": place['place_id'],
            "key": API_KEY,
        })

        log('Writing... ' + directory + '\\' + place['place_id'] + '.json', end=' ')
        print(json.dumps(my_json), file=f)
        time_end = time.time()
        execution_time = time_end - time_start
        time_sum += execution_time
        log('  time_elapsed:', execution_time, ' counter:', counter + 1)
        counter += 1

    log('Written', counter, 'files of', len(place_list['results']))
    if counter > 0:
        log('Time elapsed:', time_sum, 'with average time:', time_sum / counter)


def create_categories(categories_json):
    main_directory = os.getcwd() + '\\London' + '\\all_places'
    if not os.path.exists(main_directory):
        os.makedirs(main_directory)

    for keywords in categories_json['categories']:
        for keyword in keywords['words']:
            directory = main_directory + '\\' + keywords['name'] + '\\' + keyword
            if not os.path.exists(directory):
                os.makedirs(directory)

            my_json = get_radar_search({
                "location": London,
                "radius": "25000",
                "key": API_KEY,
                "keyword": keyword,
            })
            if my_json['status'] != 'OK':
                print("!" * 160)
                continue

            f = open(directory + '\\' + keyword + '.json', 'w')
            log("=" * 80)
            log(directory + '\\' + keyword + '.json')

            print(json.dumps(my_json), file=f)
            f.close()
            create_detail_files(keyword, directory)


if __name__ == '__main__':
    create_categories(json.loads(open('categories.json').read()))
