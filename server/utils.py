import os
import requests
import time

def _get_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def curl(url, force=False, getter=_get_url, name=None, max_age=None):
    name = url.replace("/", "_")
    try:
        os.mkdir(".ytcache")
    except FileExistsError:
        pass
    fname = os.path.join(".ytcache", "{}.html".format(name))
    if os.path.exists(fname):
        if max_age and time.time() - os.path.getmtime(fname) > max_age:
            force = True
    else:
        force = True
    if force:
        text = getter(url)
        with open(fname, "w") as _file:
            _file.write(text)
        print("downloading!", url)
        return text
    with open(fname, "r") as _file:
        return _file.read()
