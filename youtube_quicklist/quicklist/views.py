from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from googleapiclient.discovery import build
from django.conf import settings

def index(request):
    service = build('youtube', 'v3', developerKey=settings.API_KEY)
    response = service.search().list(q="clio goes two wheel", part="id", maxResults=5).execute()
    cond = 5
    videoId = response["items"][0]["id"]["videoId"]
    context = { 'cond':cond, 'videoId':videoId }
    return render(request, 'quicklist/index.html', context)