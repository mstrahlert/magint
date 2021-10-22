#!/usr/bin/env python

import configparser
import argparse
import sys
import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def parse_config(configfile):
    if os.path.exists(configfile) == False:
        print("Error: Configfile {} does not exist".format(configfile))
        sys.exit(1)

    config = configparser.ConfigParser()
    with open(configfile) as f:
        config.read_string("[global]\n" + f.read())

    for key in ['activities_url', 'api_key', 'athlete_id']:
        if key not in config['global']:
            sys.exit("Missing required option {}".format(key))

    mapping = {}
    mapping['activities_url'] = config.get('global', 'activities_url')
    mapping['api_key'] = config.get('global', 'api_key')
    mapping['athlete_id'] = config.get('global', 'athlete_id')

    return mapping

def request_activities(global_config):
    res = requests.get(global_config['activities_url'].format(athlete_id=global_config['athlete_id']), auth=('API_KEY', global_config['api_key']))

    if res.status_code == 200:
        return res
    else:
        print("Error fetching {}".format(res.url))


def main():
    parser = argparse.ArgumentParser(description='Analyze Intervals.icu Data')
    parser.add_argument('--config', action='store', default='magint.conf',
                        metavar='PATH', help='Alternate configuration file')
    parser.add_argument('--save', action='store_true', default=False,
                        help='Save content')

    results = parser.parse_args()

    global_config = parse_config(results.config)

    print(global_config)

#    sys.exit()

    my_dataset = request_activities(global_config)
    if results.save == True:
        with open(my_dataset.headers['Content-disposition'].split('=')[1], 'wb') as f:
            f.write(my_dataset.content)


#    print(my_dataset[0]["name"])
#    print(my_dataset[0]["map"]["summary_polyline"])

#    print(my_dataset)


if __name__ == "__main__":
    main()