from bs4 import BeautifulSoup
from django.core import files
from django.db import models
import re
import requests
from server.utils import get_image_url, curl, get_or_create, serialize, curl_image_to_field
import tempfile
from urllib.parse import urljoin

class Channel(models.Model):
  external_id = models.CharField(max_length=64, unique=True)
  external_username = models.CharField(max_length=128, null=True, blank=True)
  name = models.CharField(max_length=128, null=True, blank=True)
  updated = models.DateTimeField(auto_now=True)
  image = models.ImageField(upload_to='channel_images', null=True, blank=True)
  __str__ = lambda self: self.name or self.external_id

  @property
  def latest_promos(self):
    out = {}
    for video in self.video_set.all():
      for videosponsor in video.videosponsor_set.all():
        if videosponsor.sponsor_id in out:
          continue
        out[videosponsor.sponsor_id] = {
          'sponsor_id': videosponsor.sponsor_id,
          'url': videosponsor.url,
          'paragraph': videosponsor.paragraph
        }
    return list(out.values())

  @classmethod
  def from_string(cls, s):
    MATCH_URL = '"rssUrl":"https://www.youtube.com/feeds/videos.xml.channel_id=([^"]+)'
    defaults = {}
    s = s.replace('https://www.youtube.com/user', 'https://www.youtube.com')
    s = re.sub('/(featured|videos|playlists|community|store|channels|about)', '', s)
    s = s.replace('youtube.com/c/', 'youtube.com/')
    if 'youtube.com/watch?v=' in s:
      text = curl(s, max_age=3600)
      soup = BeautifulSoup(text, features='html.parser')
      channel_id = soup.find('meta', {'itemprop': 'channelId'})['content']
    elif re.match('https://www.youtube.com/([^/]*)$', s):
      channel_name = s.split('/')[-1]
      if cls.objects.filter(external_username=channel_name):
        return cls.objects.filter(external_username=channel_name)[0]
      text = curl(s, max_age=3600)
      channel_ids = re.findall(MATCH_URL, text)
      if len(set(channel_ids)) != 1:
        raise NotImplementedError("Ambiguous number of channel ids for "+s)
      channel_id = channel_ids[0]
      defaults = {'external_username': channel_name}
    elif s.startswith('https://www.youtube.com/channel/'):
      channel_id = s.split('https://www.youtube.com/channel/')[-1]

    return get_or_create(Channel, external_id=channel_id, defaults=defaults)
  @property
  def url(self):
    return f'https://www.youtube.com/channel/{self.external_id}'
  @property
  def image_url(self):
    return self.image.url if self.image else None
  def save(self, *args, **kwargs):
    if not self.image:
      self.update_image()
    super().save(*args,**kwargs)
  def update_image(self):
    text = curl(self.url)
    image_url = text.split('"avatar":{"thumbnails":[{"url":"')[1].split('"')[0]
    curl_image_to_field(image_url, self.image)
    print('Channel image set for: ', self.name)


class Video(models.Model):
  external_id = models.CharField(max_length=64, unique=True)
  title = models.CharField(max_length=264, null=True, blank=True)
  url = models.TextField()
  channel = models.ForeignKey(Channel, models.CASCADE)
  created = models.DateTimeField()
  __str__ = lambda self: self.title or self.external_id


class Sponsor(models.Model):
  name = models.CharField(max_length=128)
  image = models.ImageField(upload_to='sponsored_images', null=True, blank=True)
  __str__ = lambda self: self.name
  @property
  def sponsor_channels(self):
    out = []
    for vs in self.videosponsor_set.all():
      channel = vs.channel
      video = vs.video
      out.append({
        'id': vs.id,
        'url': vs.url,
        'channel': serialize(channel, ['id', 'name', 'image_url', 'url']),
        'video': serialize(video, ['title', 'url']),
      })
    return out
  @property
  def image_url(self):
    return self.image.url if self.image else None
  def save(self, *args, **kwargs):
    super().save(*args,**kwargs)
    if not self.image:
      self.update_image()
    super().save(*args,**kwargs)
  def update_image(self):
    for sponsordomain in self.sponsordomain_set.all():
      image_url = get_image_url(sponsordomain)
      if not image_url:
        continue
      curl_image_to_field(image_url, self.image)
      self.save()
      print('Sponsor image set for: ', self.name)
      return


class SponsorDomain(models.Model):
  domain = models.CharField(max_length=64)
  sponsor = models.ForeignKey(Sponsor, models.SET_NULL, null=True, blank=True)
  no_promo = models.BooleanField(default=False)
  urls = models.JSONField(default=list)
  __str__ = lambda self: self.domain


class VideoSponsor(models.Model):
  video = models.ForeignKey(Video, models.CASCADE)
  channel = models.ForeignKey(Channel, models.CASCADE)
  sponsor = models.ForeignKey(Sponsor, models.CASCADE)
  url = models.CharField(max_length=256)
  paragraph = models.TextField()