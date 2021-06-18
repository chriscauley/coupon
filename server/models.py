from django.db import models

class Channel(models.Model):
  external_id = models.CharField(max_length=64, unique=True)
  external_username = models.CharField(max_length=128, null=True, blank=True)
  name = models.CharField(max_length=128, null=True, blank=True)
  __str__ = lambda self: self.name or self.external_id


class Video(models.Model):
  external_id = models.CharField(max_length=64, unique=True)
  title = models.CharField(max_length=264, null=True, blank=True)
  url = models.TextField()
  channel = models.ForeignKey(Channel, models.CASCADE)
  __str__ = lambda self: self.title or self.external_id


class Sponsor(models.Model):
  name = models.CharField(max_length=128)
  image = models.ImageField(upload_to='sponsored_images', null=True, blank=True)
  __str__ = lambda self: self.name


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