__author__ = 'Kishan'

import os
import sys
import json

from FlaskApp.scripts.data_retrieval import url_requests
from FlaskApp.scripts.config import config

match_id_directory = config.match_ids_directory
match_data_directory = config.match_data_directory
progress_counter = int
max_attempts = 15


# Get json for each match id
def main():
    global progress_counter
    regions = get_match_regions()
    match_ids = get_match_ids([os.path.join(
        config.match_ids_directory, x.upper() + '.json')
                               for x in regions])
    print('\n\nGetting Match Data...\n')

    for r in range(len(match_ids)):
        progress_counter = len(match_ids[r])
        for j in range(len(match_ids[r])):
            if file_exists(regions[r], match_ids[r][j]):
                progress_counter -= 1
                progress_countdown(progress_counter, regions[r])
                continue
            match_data = get_match_data(regions[r], match_ids[r][j], progress_counter)
            progress_counter -= 1
            write_match_data(match_data, regions[r], match_ids[r][j])
            progress_countdown(progress_counter, regions[r])


# Get regions from match id JSON filenames
def get_match_regions():
    regions = []

    for f in os.listdir(match_id_directory):
        if f.endswith('.json'):
            regions.append((f[:-5]).lower())
    regions.sort()

    return regions


# Get match ids from JSON
def get_match_ids(match_id_files):
    match_ids = []

    for f in match_id_files:
        match_ids.append(json.load(open(f)))

    return match_ids


# Check if math JSON exists before retrieving it
def file_exists(region, match_id):
    return os.path.isfile(os.path.join(os.path.join
                                       (match_data_directory, region),
                                       str(match_id) + '.json'))


# Write retrieved match data to JSON
def write_match_data(match_data, region, match_id):
    with open(os.path.join(os.path.join(match_data_directory, region.upper()),
                           str(match_id) + '.json'), 'w') as outfile:
        json.dump(match_data, outfile)


# Get match data from API request
def get_match_data(region, match_id, progress_counter):
    url = url_builder(region, match_id, '/v2.2/match/')
    return url_requests.request(url, region, progress_counter)


# Build url from which to retrieve match data
def url_builder(region, match_id, api_request):
    https = 'https://'
    riot_api = '.api.pvp.net/api/lol/'
    timeline = 'true'

    return (https + region + riot_api + region + api_request +
            str(match_id) + '?includeTimeline=' + timeline + '&api_key=' +
            config.riot_api_key)


# Print progress to console
def progress_countdown(progress_counter, region):
    sys.stdout.write('\rProgress Countdown: ' + region.upper() +
                     ' ' + str(progress_counter))
    sys.stdout.flush()


if __name__ == '__main__':
    main()
