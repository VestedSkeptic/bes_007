# *********************************************************
# a_library_02/engine_permissions.py

# *********************************************************
from django.contrib.auth.models import Permission
from a_base_02.models import allViewSecurityDict, secDict

# *********************************************************
def checkUserPermissions(userRights, viewName, args, kwargs, request):

    if viewName in allViewSecurityDict:
        if userRights['value'] >= allViewSecurityDict[viewName][0]['value']: 
            return True
        else:
            if allViewSecurityDict[viewName][0] == secDict['s_owner']:
                if hasattr(allViewSecurityDict[viewName][1], 'getInstanceFromKwargs'):
                    instance = allViewSecurityDict[viewName][1].getInstanceFromKwargs(kwargs)
                elif 'object_id' in kwargs:                    
                    instance = allViewSecurityDict[viewName][1].objects.get(pk=kwargs['object_id'])
                
                if instance.auto_citizen == request.META['duo_citizen']:    
                    return True
                else:                                                       
                    return False
            else:
                return False
    else:
        print "*** checkUserPermissions error: viewName (%s) NOT found in allViewSecurityDict" % (viewName)
        return False

# *********************************************************
def setUserPermissions(request):
    if request.META['duo_citizen']:
        if   request.META['duo_citizen'].authenticated == 1:    request.META['citizen_rights'] = secDict['s_citizen']
        elif request.META['duo_citizen'].authenticated == -1:   request.META['citizen_rights'] = secDict['s_denied']
        else:                                                   request.META['citizen_rights'] = secDict['s_citPending']
    else:                           
        request.META['citizen_rights'] = secDict['s_guest']

# *********************************************************
def extract_views_from_urlpatterns(urlpatterns, base=''):
    """
    Return a list of views from a list of urlpatterns.
    Each object in the returned list is a two-tuple: (view_func, regex)
    """
    views = []
    for p in urlpatterns:
        if hasattr(p, '_get_callback'):
            try:                        views.append((p._get_callback(), base + p.regex.pattern))
            except ViewDoesNotExist:    continue
        elif hasattr(p, '_get_url_patterns'):
            try:                       patterns = p.url_patterns
            except ImportError:        continue
            views.extend(extract_views_from_urlpatterns(patterns, base + p.regex.pattern))
        else:
            raise TypeError, "%s does not appear to be a urlpattern object" % p
    return views        
    
# *********************************************************
def getViewDict():
    import urls_root    
    view_functions = extract_views_from_urlpatterns(urls_root.urlpatterns)
    viewDict = {}
    for x in view_functions:
        viewName = x[0].__name__
        # Only care about views starting with 'VIEW_' so ...
        if viewName[:5] == 'VIEW_':
            if viewDict.has_key(viewName): viewDict[viewName] += 1
            else:                          viewDict[viewName] = 1
    return viewDict