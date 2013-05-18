# *********************************************************
# a_mgrApplication_03/urls.py

# *********************************************************
from django.conf.urls.defaults import patterns, url

# *********************************************************
urlpatterns = patterns('a_mgrApplication_03.views',                           
    url(r'^$',                                                          'a_mgrApplication_03_VIEW_List',                                 name="a_mgrApplication_03_VIEW_List"),
    url(r'^add/$',                                                      'a_mgrApplication_03_VIEW_Add',                                  name="a_mgrApplication_03_VIEW_Add"),   
    url(r'^edit/(?P<object_id>\d+)/$',                                  'a_mgrApplication_03_VIEW_Edit',                                 name="a_mgrApplication_03_VIEW_Edit"),    
    url(r'^delete/(?P<object_id>\d+)/$',                                'a_mgrApplication_03_VIEW_Delete',                               name="a_mgrApplication_03_VIEW_Delete"), 
    url(r'^delete/(?P<object_id>\d+)/(?P<confirm>\S+)/$',               'a_mgrApplication_03_VIEW_Delete',                               name="a_mgrApplication_03_VIEW_DeleteConfirm"), 
    url(r'^detail/(?P<object_id>\d+)/$',                                'a_mgrApplication_03_VIEW_Detail',                               name="a_mgrApplication_03_VIEW_Detail"),
    url(r'^subscribetoggle/(?P<object_id>\d+)/$',                       'a_mgrApplication_03_VIEW_subscribetoggle',                      name="a_mgrApplication_03_VIEW_subscribetoggle"),    
    url(r'^genericUserAppSubscription/toggle/$',                        'a_mgrApplication_03_VIEW_genericUserAppSubscriptionToggle',     name="a_mgrApplication_03_VIEW_genericUserAppSubscriptionToggle"),    
    url(r'^genericUserAppVote/vote/(?P<mode>\S+)/(?P<vote>\S+)/$',      'a_mgrApplication_03_VIEW_genericUserAppVote',                   name="a_mgrApplication_03_VIEW_genericUserAppVote"),    
)