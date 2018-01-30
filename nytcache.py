from secrets import *
import requests
import json
from datetime import datetime


CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)


MAX_STALENESS = 30
def is_fresh(cache_entry):
    now = datetime.now().timestamp()
    staleness = now - cache_entry['cache_timestamp']
    return staleness > MAX_STALENESS

def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)
    if unique_ident in CACHE_DICTION:
        if is_fresh(CACHE_DICTION[unique_ident]):
            print("Getting cached data...")
            return CACHE_DICTION[unique_ident]
        else:
            pass
    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        CACHE_DICTION[unique_ident]['cache_timestamp'] = datetime.now().timestamp()
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


def get_stories(section):
    baseurl = 'https://api.nytimes.com/svc/topstories/v2/'
    extendedurl = baseurl + section + '.json'
    params={'api-key': nyt_key}
    return make_request_using_cache(extendedurl, params)

def get_headlines(nyt_results_dict):
    results = nyt_results_dict['results']
    headlines = []
    for r in results:
        headlines.append(r['title'])
    return headlines

story_list_json = get_stories('science')
headlines = get_headlines(story_list_json)
for h in headlines:
    print(h)
