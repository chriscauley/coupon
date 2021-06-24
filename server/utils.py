from bs4 import BeautifulSoup
from django.conf import settings
from django.core import files
import json
import os
import requests
import tempfile
import time
from urllib.parse import urljoin, urlencode

def serialize(obj, keys):
  return { key: getattr(obj,key) for key in keys }

def _get_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def curl(url, force=False, getter=_get_url, name=None, max_age=None):
    name = name or url.replace("/", "_")
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


def curl_image_to_field(image_url, model_field):
  response = requests.get(image_url, stream=True)
  response.raise_for_status()
  file_name = image_url.split('/')[-1]
  lf = tempfile.NamedTemporaryFile()

  for block in response.iter_content(1024 * 8):
    if not block:
      break
    lf.write(block)
  model_field.save(file_name, files.File(lf))


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

def get_channel_id_from_url(url):
  MATCH_URL = '"rssUrl":"https://www.youtube.com/feeds/videos.xml.channel_id=([^"]+)'
  defaults = {}
  s = s.replace('https://www.youtube.com/user', 'https://www.youtube.com')
  s = re.sub('/(featured|videos|playlists|community|store|channels|about)', '', s)
  s = s.replace('youtube.com/c/', 'youtube.com/')
  if 'youtube.com/watch?v=' in s:
    text = curl(s, max_age=3600)
    soup = BeautifulSoup(text, features='html.parser')
    return soup.find('meta', {'itemprop': 'channelId'})['content']
  elif re.match('https://www.youtube.com/([^/]*)$', s):
    channel_name = s.split('/')[-1]
    if cls.objects.filter(external_username=channel_name):
      return cls.objects.filter(external_username=channel_name)[0]
    text = curl(s, max_age=3600)
    channel_ids = re.findall(MATCH_URL, text)
    if len(set(channel_ids)) != 1:
      raise NotImplementedError("Ambiguous number of channel ids for "+s)
    return channel_ids[0]
  elif s.startswith('https://www.youtube.com/channel/'):
    return s.split('https://www.youtube.com/channel/')[-1]


def search_youtube(q):
  params = {
    'key': settings.YOUTUBE_API_KEY,
    'part': 'id,snippet',
    'type': 'channel',
    'q': q,
  }
  root_url = 'https://youtube.googleapis.com/youtube/v3/search?'
  text = curl(root_url + urlencode(params), name="youtube?q="+q)
  items = json.loads(text)['items']
  for item in items:
    item.update(item.pop('snippet', {}))
  return items