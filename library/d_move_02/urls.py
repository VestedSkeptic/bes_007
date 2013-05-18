# *********************************************************
# d_move_02/urls.py

# *********************************************************
from django.conf.urls.defaults import patterns, url

# *********************************************************
urlpatterns = patterns('d_move_02.views',                           
    url(r'^$',                                      'd_move_02_VIEW_home',                      name="d_move_02_VIEW_home"),
    url(r'^addLap/$'    ,                           'd_move_02_VIEW_addLap',                    name="d_move_02_VIEW_addLap"),    
)




