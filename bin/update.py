#!/usr/bin/env python3
import os, django;os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings';django.setup()
import sys

from django.core import files

from bs4 import BeautifulSoup
from server.models import Channel, Video, Sponsor, SponsorDomain, VideoSponsor
from server.utils import curl, get_or_create, get_image_url
import tempfile
import re
import requests
from urllib.parse import urljoin


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
      defaults={'title': entry.find('title').text, 'channel': channel},
    )
    description = entry.find('media:description')
    paragraphs = description.text.split('\n')
    for i, url in enumerate(re.findall('https?://.*', description.text)):
      url, domain = get_url_and_domain(url, follow=i==0)
      if not url:
        continue
      if i == 0:
        sponsordomain = get_or_create(SponsorDomain, domain=domain)
      else:
        sponsordomain = SponsorDomain.objects.filter(domain=domain).first()
      if not sponsordomain or sponsordomain.no_promo:
        continue
      if url not in sponsordomain.urls:
        url = url.replace(u'\u200b', '') # "zero width space"
        sponsordomain.urls.append(url)
        sponsordomain.save()
      if not sponsordomain.sponsor:
        print(f'Sponsor domain missing sponsor {sponsordomain.domain}', video_url)
      else:
        paragraph = next(p for p in paragraphs if url in p)
        get_or_create(
          VideoSponsor,
          video=video,
          sponsor=sponsordomain.sponsor,
          defaults={'url': url, 'paragraph': paragraph}
        )

def get_url_and_domain(url, follow):
  url = url.split(' ')[0].strip('.,')
  domain = url.split('//')[1].split('/')[0].lower()
  if domain in ['thld.co', 'ow.ly', 'bit.ly', 'cen.yt', 'tinyurl.com']:
    if not follow:
      return [None, None]
    # get real domain from url shortener service
    url2 = requests.get(url).url
    domain = url2.split('//')[1].split('/')[0].lower()
  return url, domain


if __name__ == '__main__':
  # uncomment to redownload all images
  # Sponsor.objects.all().update(image=None)
  if len(sys.argv) > 1:
    for s in sys.argv[1:]:
      Channel.from_string(s)
  for channel in Channel.objects.all():
    update_channel_from_feed(channel)
