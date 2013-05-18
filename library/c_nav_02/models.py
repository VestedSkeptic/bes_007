# *********************************************************
# c_nav_02/models.py

# *********************************************************
from a_base_02.models import a_base_02
from a_library_02 import engine_permissions
from a_mgrApplication_03.models import subscription_01
from a_mgrApplication_03.models_aux import registeredClassInfo
from django import forms
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm
from django.template import TemplateDoesNotExist
import settings

navMenu_globalDict      = {}
navMenu_localDict       = {}

# *********************************************************
class c_nav_02(a_base_02):
    pass

    # -----------------------------------------------------
    def entryInit_middlewareMethods(cls):
        mw_methods = []
        mw_methods.append([90, 'view','mw_view_navMenu_02'])
        return mw_methods 
    entryInit_middlewareMethods = classmethod(entryInit_middlewareMethods) 
    
    # -----------------------------------------------------
    def userIsGuest(request):
        if request.META['duo_citizen']: return False
        else:                           return True
    userIsGuest = staticmethod(userIsGuest)     

    # -----------------------------------------------------
    def userIsCitizen(request):
        if request.META['duo_citizen']: return True
        else:                           return False
    userIsCitizen = staticmethod(userIsCitizen)     
    
    # -----------------------------------------------------
    def register_c_nav_02_menuItems(request, navMenuList, baseClassName):
        classObj = registeredClassInfo.get_classObject_fromBaseName(baseClassName)
        
        temp_localDict = {}
        
        for x in navMenuList:
            
            # if specified determine if renderMethod   exists
            if x['renderMethod']:
                try:    
                    renderMethod = getattr(classObj, x['renderMethod'])
                except AttributeError:
                    print "*** ERROR: %s renderMethod '%s' not found" % (classObj.__name__, x['renderMethod']) 
            
            # if specified determine if criteriaMethod exists
            if x['criteriaMethod']:
                try:
                    c_nav_classObj = registeredClassInfo.get_classObject_fromBaseName('c_nav')
                    criteriaMethod = getattr(c_nav_classObj, x['criteriaMethod'])
                except AttributeError:
                    print "*** ERROR: %s criteriaMethod '%s' not found" % (classObj.__name__, x['criteriaMethod']) 
            
#            # if isLocal then parentViewList must be specified
#            if x['isLocal'] and not x['parentViewList']:
#                print "*** NOTE: %s parentViewList not specified for local menu view '%s'" % (classObj.__name__, x['view'])
#                print "          Therefore treating this as a new-ish LOCAL_ALWAYS menu item which is always displayed when current application = (%s)" % (baseClassName)
            
            # generic fields
            x['selected']       = False
            x['baseClassName']  = baseClassName
            
            # calculate reversed link if not static
            if x['required_viewParamsList']:
                x['staticLink']      = False
                x['reversedLink']    = 'failed_global_non_static_menu_item'
            else:
                x['staticLink']      = True
                x['reversedLink']    = reverse(x['view'], urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))

            if x['isLocal']:
                if temp_localDict.has_key(x['menu']):       temp_localDict[x['menu']].append(x)
                else:                                       temp_localDict[x['menu']] = [x]
            else:
                if navMenu_globalDict.has_key(x['menu']):   navMenu_globalDict[x['menu']].append(x)
                else:                                       navMenu_globalDict[x['menu']] = [x]   
                
        if len(temp_localDict): 
            navMenu_localDict[baseClassName] = temp_localDict
            
    register_c_nav_02_menuItems = staticmethod(register_c_nav_02_menuItems) 
    
    # -----------------------------------------------------
    def mw_view_navMenu_02(request, view_func, view_args, view_kwargs):
        parentIndicatedAsSelectedByFoundChildSelected       = ''
        ultimateProperParentSelectedList                    = []
        
        # First extract appropriate child entries
        if navMenu_localDict.has_key(request.META['auto_currentApp_baseName']):
            for menuType, menuList in navMenu_localDict[request.META['auto_currentApp_baseName']].items():

                # get all child entries for the currentApp current menuType (i.e. LOCAL)
                working_childMenuList           = []
                aLocalChildWasFoundSelectedAndItsParentIs    = ''
                for x in menuList:
                    if engine_permissions.checkUserPermissions(request.META['citizen_rights'], x['view'], view_args, view_kwargs, request):
                        working_childMenuList.insert(0, x)
                        if x['view'] == request.META['auto_currentView']:
                            if x['parentViewList']:
                                aLocalChildWasFoundSelectedAndItsParentIs = x['parentViewList'][0]
                    
                # extract entries which have the properParent we are looking for        
                final_working_childMenuList = []
                if working_childMenuList:
                    if aLocalChildWasFoundSelectedAndItsParentIs:   properParent = aLocalChildWasFoundSelectedAndItsParentIs
                    else:                                           properParent = request.META['auto_currentView']
                    if properParent not in ultimateProperParentSelectedList:
                        ultimateProperParentSelectedList.append(properParent)
                    
                    for x in working_childMenuList:
                        if x['view'] == request.META['auto_currentView']:
                            x['selected'] = True
                            final_working_childMenuList.insert(0, [x['priority'], x])
                        elif properParent in x['parentViewList']:                       
                            x['selected'] = False
                            final_working_childMenuList.insert(0, [x['priority'], x])
                        elif not x['parentViewList']:
                            x['selected'] = False
                            final_working_childMenuList.insert(0, [x['priority'], x])
                        
                if final_working_childMenuList:
                    final_working_childMenuList.sort()
                    renderedList = []
                    for z in final_working_childMenuList:
                        x = z[1]                        
                        if x['criteriaMethod']: # there is a displayCriteriaMethod name, use it to get the actual method from the class
                            classObj = registeredClassInfo.get_classObject_fromBaseName('c_nav')
                            displayCriteriaMethod = getattr(classObj, x['criteriaMethod'])
                            displayCriteriaOk = displayCriteriaMethod(request)
                        else:
                            displayCriteriaOk = True
                        
                        if displayCriteriaOk:
                            if x['renderMethod']: # there is a renderMethod name, use it to get the actual method from the class
                                classObj = registeredClassInfo.get_classObject_fromBaseName(x['baseClassName'])
                                renderMethod = getattr(classObj, x['renderMethod'])
                                renderedList.append(renderMethod(request, view_func, view_args, view_kwargs))
                            else:
                                try:
#                                    templateName = 'BLOCK_menu_%s.html'%(menuType)
                                    templateName = 'B_menu.html'                                    
                                    
                                    # if not a staticLink then 
                                    # verify necessary parameters can be found in view_kwargs
                                    # calculate reverseLink
                                    if not x['staticLink']:
                                        allParametersFound = True
                                        kwargs_dict = {}
                                        for param in x['required_viewParamsList']:
                                            if param not in view_kwargs: 
                                                print "*** ERROR: non-static local menu item '%s' view parameter '%s' not found in view_kwargs" % (x['view'], param)
                                                allParametersFound = False
                                            else:
                                                kwargs_dict[param] = view_kwargs[param]
                                        if allParametersFound:
                                            x['reversedLink']    = reverse(x['view'], kwargs=kwargs_dict, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))
                                    
                                    renderedList.append(c_nav_02.processTemplate_01(request, templateName, {'object': x}))
                                except TemplateDoesNotExist:
                                    renderedList.append("ERROR: %s does not exist" % (templateName))   
                    request.META['baseContext_navigationMenu_%s' % (menuType)] = ''.join(renderedList)  
                    # ----------------                           

        # Next check non-child entries for a selection match
        for menuType, menuList in navMenu_globalDict.items():
            working_nonChildMenuList  = []

            for x in menuList:
                if engine_permissions.checkUserPermissions(request.META['citizen_rights'], x['view'], view_args, view_kwargs, request):
                    working_nonChildMenuList.insert(0, [x['priority'], x])

            if working_nonChildMenuList:
                for z in working_nonChildMenuList:
                    x = z[1]
                    if x['baseClassName'] == request.META['auto_currentApp_baseName'] and x['view'] == request.META['auto_currentView'] : x['selected'] = True
                    elif x['view'] in ultimateProperParentSelectedList:                                                                   x['selected'] = True
                    else:           
                        # New-ish conditional here testing if the optional list in x['altSelectOnViewList'] contains the basename and current view. 
                        # This optional list was added April 27 and is defined in class.models and contains all the views for which this global button shoudl be selected on.
                        if x['baseClassName'] == request.META['auto_currentApp_baseName'] and request.META['auto_currentView'] in x['altSelectOnViewList']  : x['selected'] = True
                        else:                                                                                                                                 x['selected'] = False

                working_nonChildMenuList.sort()
                
                renderedList = []
                for z in working_nonChildMenuList:
                    x = z[1]
                    if x['criteriaMethod']: # there is a displayCriteriaMethod name, use it to get the actual method from the class
                        classObj = registeredClassInfo.get_classObject_fromBaseName('c_nav')
                        displayCriteriaMethod = getattr(classObj, x['criteriaMethod'])
                        displayCriteriaOk = displayCriteriaMethod(request)
                    else:
                        displayCriteriaOk = True
                    
                    if displayCriteriaOk:
                        if x['renderMethod']: # there is a renderMethod name, use it to get the actual method from the class
                            classObj = registeredClassInfo.get_classObject_fromBaseName(x['baseClassName'])
                            renderMethod = getattr(classObj, x['renderMethod'])
#                            print "+++ view_func = %s" % (view_func)
#                            print "+++ view_args = %s" % (view_args,)
#                            print "+++ view_kwargs = %s" % (view_kwargs,)
                            renderedList.append(renderMethod(request, view_func, view_args, view_kwargs))
                        else:
                            try:
#                                templateName = 'BLOCK_menu_%s.html'%(menuType)
                                templateName = 'B_menu.html'
                                
                                # ----------------- COPIED FROM LOCAL 
                                if not x['staticLink']:
                                    allParametersFound = True
                                    kwargs_dict = {}
                                    for param in x['required_viewParamsList']:
                                        if param not in view_kwargs: 
#                                            print "*** ERROR: non-static global menu item '%s' view parameter '%s' not found in view_kwargs" % (x['view'], param)
                                            allParametersFound = False
                                        else:
                                            kwargs_dict[param] = view_kwargs[param]
                                    if allParametersFound:
                                        x['reversedLink']    = reverse(x['view'], kwargs=kwargs_dict, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))                                
                                # ----------------- COPIED FROM LOCAL 
                                
                                renderedList.append(c_nav_02.processTemplate_01(request, templateName, {'object': x}))
                            except TemplateDoesNotExist:
                                renderedList.append("ERROR: %s does not exist" % (templateName))    
                request.META['baseContext_navigationMenu_%s' % (menuType)] = ''.join(renderedList)                             

        return None  
    mw_view_navMenu_02 = staticmethod(mw_view_navMenu_02)
