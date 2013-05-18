# *********************************************************
# e_thread_03/urls.py

# *********************************************************
from django.conf.urls.defaults import patterns, url

# *********************************************************
urlpatterns = patterns('e_thread_03.views',                           
    url(r'^$',                                                      'e_thread_03_VIEW_List',                         name="e_thread_03_VIEW_List"),
    url(r'^(?P<object_id>\d+)/$',                                   'e_thread_03_VIEW_Detail',                       name="e_thread_03_VIEW_Detail"),    
    url(r'^raw/(?P<object_id>\d+)/$',                               'e_thread_03_VIEW_Raw',                          name="e_thread_03_VIEW_Raw"),      
    url(r'^bbcode/(?P<object_id>\d+)/$',                            'e_thread_03_VIEW_BBcode',                       name="e_thread_03_VIEW_BBcode"),      
)