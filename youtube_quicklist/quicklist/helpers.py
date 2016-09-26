from django.conf import settings
from googleapiclient.discovery import build

def search_videos(query):
    service = build('youtube', 'v3', developerKey=settings.API_KEY)
    response = service.search().list(q=query, part="id, snippet", type="video",
        maxResults=5).execute()
    # video_id = response["items"][0]["id"]["video_id"]

    results = [{ "video_id":item["id"]["videoId"], 
                 "thumbnail_url":item["snippet"]["thumbnails"]["default"] \
                ["url"] } for item in response["items"] ]
    return results

def get_or_create_playlist(request):
    if not 'playlist' in request.session:
        request.session['playlist'] = []
    return request.session['playlist']
