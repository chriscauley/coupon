import os
import requests
import time

def _get_url(url):
    response = requests.get(url)
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
