from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from server.models import Channel, Sponsor, Video, VideoSponsor
from server.utils import serialize
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