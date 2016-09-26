from .models import User, Playlist, Results, Video

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from .helpers import *
import json

# def ajax_test(request):
#     return HttpResponse("foo")
def ajax_test(request):
    pass
    if not "asdf" in request.session:
        request.session["asdf"] = 1
    else:
        request.session["asdf"] += 2
    test_data = {'a':'aaa','b':'bbb','c':'ccc'}
    a = json.dumps(test_data)
    return HttpResponse(a)

def index(request):
    query = request.GET.get("query", False)
    if query:
        results = search_videos(query)
        request.session["results"] = results
        if request.is_ajax():
            if request.GET["need_html_results"] == "true":
                results = render_to_string("quicklist/search_results.html", 
                                            context=None, request=request)
            response_data = {"results": results}
            return HttpResponse(json.dumps(response_data))
    current_video_id = ""
    playlist_exists = False
    if "current_video_index" not in request.session:
        request.session["current_video_index"] = 0
    playlist = get_or_create_playlist(request)
    print(playlist)
    if len(playlist) > 0:
        playlist_exists = True
        current_video_id = playlist[request.session["current_video_index"]] \
                                                   ["video_id"]
    

    request.session["playlist"] = playlist
    context = { 'playlist': playlist, 'current_video_id': current_video_id,
                'playlist_exists': playlist_exists }
    return render(request, 'quicklist/index.html', context)

def play_next(request):
    pass

def add(request):
    rs = request.session
    add_video_index = int(request.GET["add_video_index"])
    playlist = get_or_create_playlist(request)
    rs['playlist'].append(rs["results"][add_video_index])
    rendered_playlist = render_to_string("quicklist/playlist.html", 
                                     context=None, request=request)
    return HttpResponse(json.dumps(rendered_playlist))
    # return redirect(reverse("index"))

def next_video(request):
    request.session["current_video_index"] += 1
    if request.session["current_video_index"] >= \
       len(request.session["playlist"]):
        request.session["current_video_index"] = 0
    return redirect(reverse("index"))


def remove(request):
    playlist = get_or_create_playlist(request)
    item_for_removal = int(request.GET["remove_video_index"])
    del playlist[item_for_removal]
    request.session['playlist'] = playlist
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
