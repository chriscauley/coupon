#!/usr/bin/env python3
import os, django;os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings';django.setup()

from bs4 import BeautifulSoup
from server.utils import curl
from server.models import Channel, Video, Sponsor, SponsorDomain, VideoSponsor
import re
import requests

def get_or_create(model, defaults={}, **kwargs):
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


for channel in Channel.objects.all():
  url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel.external_id}'
  text = curl(url, max_age=3600) # reupdate every hour
  soup = BeautifulSoup(text, features='html.parser')
  if not channel.name:
    channel.name = soup.find('title').text
    channel.save()
  for entry in soup.findAll('entry'):
    video_url = entry.find('link')['href']
    video = get_or_create(
      Video,
      external_id=video_url.split('?v=')[1],
      url=video_url,
      defaults={'title': entry.find('title').text},
    )
    description = entry.find('media:description')
    for i, url in enumerate(re.findall('https?://.*', description.text)):
      url = url.split(' ')[0].strip('.')
      domain = url.split('//')[1].split('/')[0]
      if domain == 'thld.co' or domain == 'ow.ly':
        continue # TODO redirects
      if i == 0:
        sponsordomain = get_or_create(SponsorDomain, domain=domain)
      else:
        sponsordomain = SponsorDomain.objects.filter(domain=domain).first()
      if not sponsordomain or sponsordomain.no_promo:
        continue
      if url not in sponsordomain.urls:
        sponsordomain.urls.append(url)
        sponsordomain.save()
      if not sponsordomain.sponsor:
        print(f'Sponsor domain missing sponsor {sponsordomain.domain}', video_url)
      else:
        get_or_create(VideoSponsor, video=video, sponsor=sponsordomain.sponsor)