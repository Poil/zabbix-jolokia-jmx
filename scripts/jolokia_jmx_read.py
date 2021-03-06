#!/usr/bin/python
import urllib.request
import json
import sys
import base64

#verify we have at least two arguments
if len(sys.argv) < 3:
    print("at least two arguments required!")
    exit(1)

attr = sys.argv[1].replace(' ','%20')
key = sys.argv[2].replace(' ','%20')

#see if arg3 exists, if not then use 13337 as the default port
try:
    port = sys.argv[3]
except IndexError:
    port = "8080"

#argument 1 is the bean
#argument 2 is the key
url = "http://localhost:" + port + "/jolokia/read/" + attr + "/" + key

if len(sys.argv) >= 5:
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, sys.argv[4], sys.argv[5])
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

    proxy_support = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(handler, proxy_support)

page = opener.open(url).read()

#put in the response dictionary
resp_dict = json.loads(page)

#log what happened, this is for testing.  Also let Zabbix know that the item sent was not supported.
if resp_dict['status'] != 200:
    print("ZBX_NOTSUPPORTED")
    exit()

print(resp_dict['value'])
