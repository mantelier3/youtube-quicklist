from .models import User, Playlist, Results, Video

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from .helpers import *

def index(request):
    current_video_id = ""
    playlist_exists = False
    print("PLAYLIST IS FALSE")
    if "current_video_index" not in request.session:
        request.session["current_video_index"] = 0
    playlist = get_or_create_playlist(request)
    print(playlist)
    if len(playlist) > 0:
        playlist_exists = True
        print("PLAYLIST IS TRUE I MEAN IT'S NOT EMPTY IT ACTUALLY EXISTS")
        current_video_id = playlist[request.session["current_video_index"]]["video_id"]
    query = request.GET.get("query", False)
    if query:
        results = search_videos(query)
        request.session["results"] = results
    request.session["playlist"] = playlist
    context = { 'playlist': playlist, 'current_video_id': current_video_id, 'playlist_exists': playlist_exists }
    return render(request, 'quicklist/index.html', context)

def play_next(request):
    pass

def add(request):
    rs = request.session
    video_id = int(request.GET.get("video_id"))
    playlist = get_or_create_playlist(request)
    playlist.append(rs["results"][video_id])
    request.session['playlist'] = playlist
    return redirect(reverse("index"))

def next_video(request):
    request.session["current_video_index"] += 1
    if request.session["current_video_index"] >= len(request.session["playlist"]):
        request.session["current_video_index"] = 0
    return redirect(reverse("index"))


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

def clear_playlist(request):
    del request.session["playlist"]
    return redirect(reverse("index"))

def clear_session(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect(reverse("index"))
