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

def fetch_metadata(u=url, f=filename):
    r = requests.get(u)
    with open(f, 'wb') as fd:
        for chunk in r.iter_content(4096):
            fd.write(chunk)

def add_commit_push(f=filename, c='Metadata timestampted at ' + url_date.isoformat()):
    repo.index.add([f])
    repo.index.commit(c)
    repo.remotes.origin.push() 


# Only needed at the very start
if not Path(filename).is_file():
    fetch_metadata()



file_date = utc.localize(datetime.datetime.utcfromtimestamp(os.path.getmtime(filename)))



if url_date > file_date:
    fetch_metadata()


repo = Repo('.')

if repo.is_dirty(untracked_files=True):
    if filename in repo.untracked_files:
#        repo.index.add([filename])
#        repo.index.commit('Metadata timestamped at ' + url_date.isoformat())
        add_commit_push()

if filename in [ item.a_path for item in repo.index.diff(None) ]:
#    repo.index.add([filename])
#    repo.index.commit('Metadata timestamped at ' + url_date.isoformat())
    add_commit_push()
