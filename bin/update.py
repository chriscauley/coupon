#!/usr/bin/env python3
import os, django;os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings';django.setup()
import sys

from django.core import files

from bs4 import BeautifulSoup
from server.models import Channel, Video, Sponsor, SponsorDomain, VideoSponsor
from server.utils import curl
import tempfile
import re
import requests
from urllib.parse import urljoin

MATCH_URL = '"rssUrl":"https://www.youtube.com/feeds/videos.xml.channel_id=([^"]+)'


def goc_channel_from_string(s):
  defaults = {}
  s = s.replace('https://www.youtube.com/user', 'https://www.youtube.com')
  s = re.sub('/(featured|videos|playlists|community|store|channels|about)', '', s)
  s = s.replace('youtube.com/c/', 'youtube.com/')
  if re.match('https://www.youtube.com/([^/]*)$', s):
    channel_name = s.split('/')[-1]
    if Channel.objects.filter(external_username=channel_name):
      return Channel.objects.filter(external_username=channel_name)[0]
    text = curl(s, max_age=3600)
    channel_ids = re.findall(MATCH_URL, text)
    if len(set(channel_ids)) != 1:
      raise NotImplementedError("Ambiguous number of channel ids for "+s)
    channel_id = channel_ids[0]
    defaults = {'external_username': channel_name}
  elif s.startswith('https://www.youtube.com/channel/'):
    channel_id = s.split('https://www.youtube.com/channel/')[-1]

  return get_or_create(Channel, external_id=channel_id, defaults=defaults)


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


def update_channel_from_feed(channel):
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
      url = url.replace(u'\u200b', '') # "zero width space"
      domain = url.split('//')[1].split('/')[0].lower()
      if domain in ['thld.co', 'ow.ly', 'bit.ly', 'cen.yt']:
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


def update_sponsor(sponsor):
  if not sponsor.image:
    for sponsordomain in sponsor.sponsordomain_set.all():
      image_url = get_image_url(sponsordomain)
      if image_url:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        file_name = image_url.split('/')[-1]
        lf = tempfile.NamedTemporaryFile()

        for block in response.iter_content(1024 * 8):
          if not block:
              break
          lf.write(block)

        sponsor.image.save(file_name, files.File(lf))
        sponsor.save()
        print('Sponsor image set for: ', sponsor)

if __name__ == '__main__':
  # uncomment to redownload all images
  # Sponsor.objects.all().update(image=None)
  if len(sys.argv) > 1:
    for s in sys.argv[1:]:
      goc_channel_from_string(s)
  for channel in Channel.objects.all():
    update_channel_from_feed(channel)
  for sponsor in Sponsor.objects.all():
    update_sponsor(sponsor)