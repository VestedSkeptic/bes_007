# *********************************************************
# a_update_02/urls.py

# *********************************************************
from django.conf.urls.defaults import patterns, url

# *********************************************************
urlpatterns = patterns('a_update_02.views',                           
    url(r'^$',                                    'a_update_02_VIEW_List',            name="a_update_02_VIEW_List"),
    url(r'^add/$',                                'a_update_02_VIEW_Add',             name="a_update_02_VIEW_Add"),     
    url(r'^reset/(?P<scriptName>\S+)/$',          'a_update_02_VIEW_ResetTo',         name="a_update_02_VIEW_ResetTo"),     
    url(r'^contents/(?P<scriptName>\S+)/$',       'a_update_02_VIEW_Contents',        name="a_update_02_VIEW_Contents"),     
)  