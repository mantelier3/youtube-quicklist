from .models import User, Playlist, Results, Video

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from .helpers import * # need to change so it doesn't contain app name - tincek fixed

def index(request):
    playlist = get_or_create_playlist(request)
    query = request.GET.get('query','clio goes two wheel')
    results = search_videos(query)
    request.session["results"] = results
    context = { 'playlist': playlist, 'video_id':results[0]["video_id"],
                'results':results }
    #return HttpResponse(playlist)
    return render(request, 'quicklist/index.html', context)

def add(request):
    rs = request.session
    video_id = int(request.GET.get("video_id"))
    playlist = get_or_create_playlist(request)
    #playlist.append({'thumbnail_url': })
    playlist.append(rs["results"][video_id])
    request.session['playlist'] = playlist
    # request.session['playlist'] = []
    return redirect(reverse("index"))
    # return HttpResponse(request.GET.get("video_id"))
    # return HttpResponse(', '.join(playlist))

def remove(request):
    playlist = get_or_create_playlist(request)
    playlist.remove(request.GET.get("video_id")) # will error if video_id is not in playlist
    # request.session['playlist'] = playlist # clear playlist
    return redirect(reverse("index"))

def asdf(request):
    if 'count' in request.session:
        request.session['count'] += 1
        return HttpResponse('new count=%s' % request.session['count'])
    else:
        request.session['count'] = 1
        return HttpResponse('No count in session. Setting to 1')

def clear_playlsit(request):
    del request.session["playlist"]
    return redirect(reverse("index"))
