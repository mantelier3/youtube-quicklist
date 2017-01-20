# from .models import User, Playlist, Results, Video

from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render, redirect
# from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from .helpers import *
import json

# def ajax_test(request):
#     return HttpResponse("foo")


def index(request):
    request.session["TEST"] = "TRUE"
    query = request.GET.get("query", False)
    if query:
        results = search_videos(query)
        request.session["results"] = results
        request.session.save()
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
        current_video_id = playlist[request.session[
            "current_video_index"]]["video_id"]
    request.session["playlist"] = playlist
    context = {'playlist': playlist,
               'current_video_id': current_video_id,
               'playlist_exists': playlist_exists,
               'start_number': 0}
    return render(request, 'quicklist/index.html', context)


def add(request, position, result_index):
    print("foobar1234 {} {}".format(position, result_index))
    playlist = get_or_create_playlist(request)
    new_video = request.session["results"][int(result_index)]
    playlist.append(new_video)
    request.session['playlist'] = playlist
    print("session playlist", request.session["playlist"])
    request.session.save()
    rendered_item = render_to_string("quicklist/playlist.html",
                                     context={"playlist": [new_video],
                                              "start_number": position},
                                     request=request)
    # return HttpResponse("hello")
    # return HttpResponse("aaaaaaaaaaaaaaaaaaa")
    return HttpResponse(json.dumps({"rendered_item": rendered_item,
                                    "position": position}))


def remove(request, position):
    playlist = get_or_create_playlist(request)
    print("PLAYLIST IS A")
    print(playlist)
    # video_index_remove = int(request.GET["video_index_remove"])
    print("video_index_remove is", position)
    del playlist[int(position)]
    request.session['playlist'] = playlist
    request.session.save()
    # rendered_playlist = render_to_string("quicklist/playlist.html",
    #                                      context={"playlist": playlist},
    #                                      request=request)
    return HttpResponse(position)


def next_video(request):
    if "current_video_index" not in request.session:
        request.session["current_video_index"] = 0
    playlist = get_or_create_playlist(request)
    request.session["current_video_index"] += 1
    if request.session["current_video_index"] >= len(playlist):
        request.session["current_video_index"] = 0
    print(playlist)
    if len(playlist) > 0:
        # playlist_exists = True
        current_video_id = playlist[request.session[
            "current_video_index"]]["video_id"]
    return HttpResponse(json.dumps(current_video_id))

    # request.session["current_video_index"] += 1
    # if request.session["current_video_index"] >= \
    #    len(request.session["playlist"]):
    #     request.session["current_video_index"] = 0
    # return redirect(reverse("index"))


def clear_playlist(request):
    del request.session["playlist"]
    return redirect(reverse("index"))


def clear_session(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect(reverse("index"))


def asdf(request):
    if 'count' in request.session:
        request.session['count'] += 1
        return HttpResponse('new count=%s' % request.session['count'])
    else:
        request.session['count'] = 1
        return HttpResponse('No count in session. Setting to 1')


def ajax_test(request):
    pass
    if "asdf" not in request.session:
        request.session["asdf"] = 1
    else:
        request.session["asdf"] += 2
    test_data = {'a': 'aaa', 'b': 'bbb', 'c': 'ccc'}
    a = json.dumps(test_data)
    return HttpResponse(a)


def play_next(request):
    pass
