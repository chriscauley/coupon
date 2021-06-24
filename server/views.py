from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
import re

from server.models import Channel, Sponsor, Video, VideoSponsor
from server.utils import serialize, get_channel_id_from_url, search_youtube
from unrest.pagination import paginate


def channel_list(request):
  query = Channel.objects.all().prefetch_related('video_set')
  process = lambda o: serialize(o, ['name', 'id', 'latest_promos', 'image_url'])
  return JsonResponse(paginate(query, process=process, query_dict=request.GET, per_page=30))


def sponsor_list(request):
  query = Sponsor.objects.all()
  process = lambda o: serialize(o, ['name', 'image_url', 'id', 'sponsor_count'])
  return JsonResponse(paginate(query, process=process, query_dict=request.GET, per_page=60))


def sponsor_detail(request, sponsor_id):
  sponsor = get_object_or_404(Sponsor, id=sponsor_id)
  return JsonResponse(serialize(sponsor, ['name', 'image_url', 'id', 'sponsor_channels']))


def search_channels(request):
  return JsonResponse({'results': search_youtube(request.GET.get('q'))})


def add_channel(request):
  data = json.loads(request.body.decode("utf-8"))
  q = data.get('q')
  index = data.get('index')
  youtube_data = search_youtube(q)[index]
  channel, new = Channel.objects.get_or_create(external_id=youtube_data['channelId'])
  return JsonResponse(dict(name=youtube_data['title'], id=channel.id, new=new))
