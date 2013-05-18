# *********************************************************
# a_mgrSidebar_02/models.py

# *********************************************************
from a_base_02.models import a_base_02, secDict
from a_mgrApplication_03.models import subscription_01
from a_mgrApplication_03.models_aux import registeredClassInfo
import settings

sbMethods = []          # [0] is the index for sorthing, [1] is the full dict with all info about the method

# *********************************************************
class a_mgrSidebar_02(a_base_02):
    pass

    # -----------------------------------------------------
    def entryInit_middlewareMethods(cls):
        mw_methods = []
        mw_methods.append([90, 'view','mw_view_sidebar_methods'])
        return mw_methods 
    entryInit_middlewareMethods = classmethod(entryInit_middlewareMethods)     

    # -----------------------------------------------------
    def register_sidebarMethods(sb_methods_list, className):
        for x in sb_methods_list:
            x['className'] = className
            sbMethods.append([x['index'], x])
            sbMethods.sort()      # hack to sort the items by index. I didn't bother to find a better place to put this as this only happens at __new__
    register_sidebarMethods = staticmethod(register_sidebarMethods)         

    # -----------------------------------------------------
    def mw_view_sidebar_methods(request, view_func, view_args, view_kwargs):
        request.META['a_mgrSidebar_displayList'] = []

        # get a list of applications citizen is subscribed to
        subscribedApplicationsByBaseName = []
        QS = subscription_01.objects.filter(auto_citizen__exact=request.META['duo_citizen'])
        for x in QS:
            subscribedApplicationsByBaseName.append(x.application.basename)
            
        for x in sbMethods:
            methodDict = x[1]
            securityAccessGranted = False

            if request.META['citizen_rights']['value'] >= secDict[methodDict['security']]['value']:            
                securityAccessGranted = True
            elif methodDict['security'] == 's_subscribed' and request.META['citizen_rights']['value'] >= secDict['s_citizen']['value']: # because only citizens can subscribe
                if methodDict['className'] in subscribedApplicationsByBaseName:
                    securityAccessGranted = True
                         
            if securityAccessGranted:
                # Now see if this sidebar method should be displayed by the view and app we are in
                
                displayByCurrentSiteLocation = True
                if methodDict['valid_app_baseName_list']:
                    if request.META['auto_currentApp_baseName'] not in methodDict['valid_app_baseName_list']:
                        displayByCurrentSiteLocation = False
#                        print "*** displayByCurrentSiteLocation FAILED because current app (%s) is not in valid_app_baseName_list" % (request.META['auto_currentApp_baseName'])
                elif methodDict['valid_view_list']:
                    if request.META['auto_currentView'] not in methodDict['valid_view_list']:
                        displayByCurrentSiteLocation = False
#                        print "*** displayByCurrentSiteLocation FAILED because current view (%s) is not in valid_view_list" % (request.META['auto_currentView'])

                if displayByCurrentSiteLocation:
                    classObj = registeredClassInfo.get_classObject_fromBaseName(methodDict['className'])
                    sbMethod = getattr(classObj, methodDict['methodName'])
#                    request.META['a_mgrSidebar_displayList'].append(sbMethod(request, view_func, view_args, view_kwargs))
                    sbReturn = sbMethod(request, view_func, view_args, view_kwargs)
                    if sbReturn:
                        request.META['a_mgrSidebar_displayList'].append(sbReturn)
                    

            else:
#                print "*** mw_view_sidebar_methods: Insufficient security for %s" % (methodDict['methodName'])
                pass
        return None  
    mw_view_sidebar_methods = staticmethod(mw_view_sidebar_methods)