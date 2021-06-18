from django.http import JsonResponse

from server.models import Channel, Sponsor, Video, VideoSponsor
from unrest.pagination import paginate


def serialize(obj, keys):
  return { key: getattr(obj,key) for key in keys }


def channel_list(request):
  query = Channel.objects.all().prefetch_related('video_set')
  process = lambda o: serialize(o, ['name', 'id', 'latest_promos'])
  return JsonResponse(paginate(query, process=process, query_dict=request.GET, per_page=30))


def sponsor_list(request):
  query = Sponsor.objects.all()
  process = lambda o: serialize(o, ['name', 'image_url', 'id'])
  return JsonResponse(paginate(query, process=process, query_dict=request.GET, per_page=60))

