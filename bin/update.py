#!/usr/bin/env python3
import os, django;os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings';django.setup()
import sys

from django.core.cache import cache

from server.models import Channel, Sponsor
from server.utils import get_or_create, get_channel_id_from_url

if __name__ == '__main__':
  # uncomment to redownload all images
  # Sponsor.objects.all().update(image=None)
  if len(sys.argv) > 1:
    for s in sys.argv[1:]:
      get_or_create(Channel, external_id=get_channel_id_from_url(s))
  for channel in Channel.objects.all():
    channel.update_from_feed()
  cache.clear()
  for sponsor in Sponsor.objects.all():
    sponsor.sponsor_channels # refill cache
    sponsor.save() # get missing images
