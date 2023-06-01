#!/usr/bin/env python3

import json
import re
from configparser import ConfigParser
from os import unlink
from subprocess import run
from urllib.request import urlopen

GITHUB_API = "https://api.github.com/repos/{}/releases/latest"


def main():
    config = ConfigParser()
    config.read("config.ini")

    for repo, pattern in config['targets'].items():
        resp = json.load(urlopen(GITHUB_API.format(repo)))
        pattern = re.compile(pattern)
        for asset in resp['assets']:
            if pattern.search(asset['name']):
                print(f"Downloading {asset['name']}")
                print(asset['name'], asset['browser_download_url'])
                run(["curl", "-L", "-o", asset['name'], asset['browser_download_url']])
                print(f"Uploading {asset['name']}")
                run(["curl", "-F", f"package=@{asset['name']}", f"https://{config['gemfury']['token']}@push.fury.io/nattofriends/"])
                unlink(asset['name'])



if __name__ == '__main__':
    main()
