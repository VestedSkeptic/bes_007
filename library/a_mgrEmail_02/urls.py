# *********************************************************
# a_mgrEmail_02/urls.py

# *********************************************************
from django.conf.urls.defaults import patterns, url

# *********************************************************
urlpatterns = patterns('a_mgrEmail_02.views',                           
    url(r'^$',                                                      'a_mgrEmail_02_VIEW_List',                          name="a_mgrEmail_02_VIEW_List"),
    url(r'^(?P<userId>\d+)/(?P<rand1>\d+)/(?P<rand2>\d+)/$',        'a_mgrEmail_02_VIEW_ValidateEmail',                 name="a_mgrEmail_02_VIEW_ValidateEmail"), 
)
