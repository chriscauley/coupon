from bs4 import BeautifulSoup
import os
import requests
import time
from urllib.parse import urljoin

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

def get_or_create(model, defaults={}, **kwargs):
  # like django's get_or_create, but updates defaults if changed
  obj, new = model.objects.get_or_create(defaults=defaults, **kwargs)
  if new:
    attrs = {**defaults, **kwargs}
    print(f'{model.__name__} created: {obj} {attrs}')
  else:
    changed = {}
    for key, value in defaults.items():
      if getattr(obj, key) != value:
        setattr(obj, key, value)
        changed[key] = value
    if changed:
      obj.save()
      print(f'{model.__name__} updated: {obj} {changed}')
  return obj


def get_image_url(sponsordomain):
  url = 'https://'+sponsordomain.domain
  try:
    text = curl(url)
  except requests.exceptions.HTTPError as e:
    print('Unable to curl: ', sponsordomain.domain, e)
    return
  url = requests.get(url).url
  soup = BeautifulSoup(text, features='html.parser')
  link = soup.find('link', { 'rel': "apple-touch-icon" })
  link = link or soup.find('link', { 'rel': "icon" })
  if link:
    return urljoin(url, link['href'])