# *********************************************************
# a_citizen_02/urls.py

# *********************************************************
from django.conf.urls.defaults import patterns, url

# *********************************************************
urlpatterns = patterns('a_citizen_02.views',                           
    url(r'^$',                                                      'a_citizen_02_VIEW_List',                               name="a_citizen_02_VIEW_List"),
    url(r'^r/$',                                                    'a_citizen_02_VIEW_Register',                           name="a_citizen_02_VIEW_Register"),   
    url(r'^r/(?P<cit_id>\d+)/(?P<rv1>\d+)/(?P<rv2>\d+)/$',          'a_citizen_02_VIEW_Register',                           name="a_citizen_02_VIEW_Register"), 
    url(r'^(?P<object_id>\d+)/$',                                   'a_citizen_02_VIEW_Detail',                             name="a_citizen_02_VIEW_Detail"), 
    url(r'^welcome/$',                                              'a_citizen_02_VIEW_Welcome',                            name="a_citizen_02_VIEW_Welcome"),
    url(r'^logout/$',                                               'a_citizen_02_VIEW_Logout',                             name="a_citizen_02_VIEW_Logout"),      
    url(r'^authenticate/$',                                         'a_citizen_02_VIEW_Authenticate',                       name="a_citizen_02_VIEW_Authenticate"),      
    url(r'^edit/(?P<object_id>\d+)/$',                              'a_citizen_02_VIEW_Edit',                               name="a_citizen_02_VIEW_Edit"),    
    url(r'^settings/$',                                             'a_citizen_02_VIEW_Preferences',                        name="a_citizen_02_VIEW_Preferences"),      
    url(r'^editPassword/$',                                         'a_citizen_02_VIEW_PreferencesEditPassword',            name="a_citizen_02_VIEW_PreferencesEditPassword"),      
    url(r'^editEmail/$',                                            'a_citizen_02_VIEW_PreferencesEditEmail',               name="a_citizen_02_VIEW_PreferencesEditEmail"),      
    url(r'^passChange/$',                                           'a_urlPassChange_02_VIEW_List',                         name="a_urlPassChange_02_VIEW_List"),
    url(r'^recoverPassword/$',                                      'a_urlPassChange_02_VIEW_changeRequest',                name="a_urlPassChange_02_VIEW_changeRequest"),
    url(r'^recoverPasswordSent/$',                                  'a_urlPassChange_02_VIEW_changeRequestSent',            name="a_urlPassChange_02_VIEW_changeRequestSent"),
    url(r'^(?P<userId>\d+)/(?P<rand1>\d+)/(?P<rand2>\d+)/$',        'a_urlPassChange_02_VIEW_validateEmail',                name="a_urlPassChange_02_VIEW_validateEmail"), 
    url(r'^anotherEmailValidation/$',                               'a_citizen_02_VIEW_AnotherEmailValidation',             name="a_citizen_02_VIEW_AnotherEmailValidation"),      
    url(r'^anotherAuthorization/$',                                 'a_citizen_02_VIEW_AnotherAuthorization',               name="a_citizen_02_VIEW_AnotherAuthorization"),      
#    url(r'^dumpCats/(?P<object_id>\d+)/$',                          'a_citizen_02_VIEW_PreferencesEditDumpCategories',      name="a_citizen_02_VIEW_PreferencesEditDumpCategories"),      
)
