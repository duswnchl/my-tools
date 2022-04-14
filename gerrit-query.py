#!/usr/bin/python3

import json
import requests
import sys
import urllib

# frequently used queries
#   hashtag:lacros-move
#   owner:ychoi@igalia.com
#   mergedbefore:2022-04-01
#   mergedafter:2022-04-05


def add_dicts(dicts, key, values):
    if key not in dicts:
        dicts[key] = list()
    dicts[key].append(values)
    return add_dicts


SERVER_HOST = "https://chromium-review.googlesource.com"

# create payload
payload = {'q': '+'.join(sys.argv[1:])}
payload_encoded = urllib.parse.urlencode(payload, safe=':+')

response = requests.get(SERVER_HOST+"/changes/", params=payload_encoded)

# print query results
print("GET", response.url)
results = json.loads(response.content[5:])

print("Found", len(results), "CLs from gerrit....")

cl_lists = {}
for data in results:
    add_dicts(cl_lists, data['owner']['_account_id'], data['subject'])

for key in cl_lists:
    name = (requests.get(SERVER_HOST+"/accounts/"+str(key)+"/name").content[5:]
            .decode('ascii')
            .strip('\n'))
    print("\n", name, "(%d)" % len(cl_lists[key]))
    print("\n".join(cl_lists[key]))
