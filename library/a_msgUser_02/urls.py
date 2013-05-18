# *********************************************************
# a_msgUser_02/urls.py

# *********************************************************
from django.conf.urls.defaults import patterns, url

# *********************************************************
urlpatterns = patterns('a_msgUser_02.views',                           
    url(r'^$',                                                      'a_msgUser_02_VIEW_List',                           name="a_msgUser_02_VIEW_List"),
    url(r'^delete/(?P<object_id>\d+)/$',                            'a_msgUser_02_VIEW_Delete',                         name="a_msgUser_02_VIEW_Delete"), 
    url(r'^delete/(?P<object_id>\d+)/(?P<confirm>\S+)/$',           'a_msgUser_02_VIEW_Delete',                         name="a_msgUser_02_VIEW_DeleteConfirm"), 
    url(r'^detail/(?P<object_id>\d+)/$',                            'a_msgUser_02_VIEW_Detail',                         name="a_msgUser_02_VIEW_Detail"), 
    url(r'^toggleRead/(?P<object_id>\d+)/$',                        'a_msgUser_02_VIEW_ToggleRead',                     name="a_msgUser_02_VIEW_ToggleRead"),
    url(r'^gm/$',                                                   'a_msgUser_global_02_VIEW_List',                    name="a_msgUser_global_02_VIEW_List"),
    url(r'^gm/add/$',                                               'a_msgUser_global_02_VIEW_Add',                     name="a_msgUser_global_02_VIEW_Add"),   
    url(r'^gm/edit/(?P<object_id>\d+)/$',                           'a_msgUser_global_02_VIEW_Edit',                    name="a_msgUser_global_02_VIEW_Edit"),    
    url(r'^gm/delete/(?P<object_id>\d+)/$',                         'a_msgUser_global_02_VIEW_Delete',                  name="a_msgUser_global_02_VIEW_Delete"), 
    url(r'^gm/delete/(?P<object_id>\d+)/(?P<confirm>\S+)/$',        'a_msgUser_global_02_VIEW_Delete',                  name="a_msgUser_global_02_VIEW_DeleteConfirm"), 
    url(r'^gm/detail/(?P<object_id>\d+)/$',                         'a_msgUser_global_02_VIEW_Detail',                  name="a_msgUser_global_02_VIEW_Detail"),      
)