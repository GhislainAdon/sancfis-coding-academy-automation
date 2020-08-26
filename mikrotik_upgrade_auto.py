#!/usr/bin/python3
# $ usage : python mikrotik_upgrade_auto.py host/IP USER PASSWORD

import routeros # Mikrotik API
import requests # HTTP
import sys

# Make sure all arguments needed are passed correctly
try:
    host = sys.argv[1] # Get the host name or IP @ from the command line argument
except:
    print("Router Host name or IP Needed as first argument. Usage : python mikrotik_upgrade_auto.py host/IP USER PASSWORD")
    sys.exit(1)

try:
    admin_user = sys.argv[2] # Get the admin username from the command line argument
except:
    print("Admin username Needed as second argument. Usage : python mikrotik_upgrade_auto.py host/IP USER PASSWORD")
    sys.exit(1)
try:
    admin_password = sys.argv[3] # Get the admin password from the command line argument
except:
    print("Admin password Needed as third argument. Usage : python mikrotik_upgrade_auto.py host/IP USER PASSWORD")
    sys.exit(1)


try:
    api = routeros.Api(host, 8728, usessl=False, sslverify=False); # Making sure the Host is reachable
except:
    print("API Connexion Error")
    sys.exit(1)

ret = api.login(admin_user, admin_password) # Get the login status
if not ret:
    print("API Login Error")
    sys.exit(1)

ret, resp = api.find('/system/package/update') # Update the host
if not ret:
    print("API Error")
    sys.exit(1)

installed_version = resp[0]["installed-version"] # Get the installed version
major_version = installed_version.split('.')[0]
channel = resp[0]["channel"]

comp = "" # Make sure it's not the latest one already
if channel == "release-candidate":
    comp = "rc"

url = "http://download2.mikrotik.com/routeros/LATEST.{}{}".format(major_version, comp) # Get the new release candidate
try:
    httpreq = requests.get(url)
except:
    print("HTTP Request Error")
    sys.exit(1)

if httpreq.status_code == 200:
    if httpreq.text.split(" ")[0] != installed_version:
        print("1")
        sys.exit(0)
    else:
        print("0")
        sys.exit(0)
else:
    print("HTTP Return Error")
    sys.exit(1)