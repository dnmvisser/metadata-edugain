#!/usr/bin/env python3
'''Poll eduGAIN metadata and commit to git repository



'''

import os
import requests
import datetime
import pytz
from pathlib import Path
from dateutil.parser import parse as parsedate
from git import Repo

utc=pytz.UTC

url = 'https://mds.edugain.org/edugain-v1.xml'
filename=Path(url).name

r = requests.head(url)
url_date = parsedate(r.headers['last-modified'])

file_date = utc.localize(datetime.datetime.utcfromtimestamp(os.path.getmtime(filename)))


if url_date > file_date:
    r = requests.get(url)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(4096):
            fd.write(chunk)


repo = Repo('.')
if filename in [ item.a_path for item in repo.index.diff(None) ]:
    repo.index.add([filename])
    repo.index.commit('Metadata timestamped at ' + url_date.isoformat())
