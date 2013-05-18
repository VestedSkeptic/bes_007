# *********************************************************
# a_msgSocial_02/urls.py

# *********************************************************
from django.conf.urls.defaults import patterns, url

# *********************************************************
urlpatterns = patterns('a_msgSocial_02.views',                           
    url('^$',                                             'a_msgSocial_02_VIEW_List',                         name="a_msgSocial_02_VIEW_List"),
)