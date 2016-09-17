from django.conf.urls import include, patterns, url
from . import views
from django.conf import settings


urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name=''),
    url(r'^add$', views.add, name=''),
    url(r'^remove$', views.remove, name=''),
    url(r'^asdf$', views.asdf, name=''),
    url(r'^clear_playlist$', views.clear_playlsit, name=''),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]