from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from googleapiclient.discovery import build
from django.conf import settings

def index(request):
    service = build('youtube', 'v3', developerKey=settings.API_KEY)
    cond = 5
    query = request.GET.get('query','clio goes two wheel')
    response = service.search().list(q=query, part="id", maxResults=5).execute()
    videoId = response["items"][0]["id"]["videoId"]
    context = { 'cond':cond, 'videoId':videoId, 'query':query}
    return render(request, 'quicklist/index.html', context)