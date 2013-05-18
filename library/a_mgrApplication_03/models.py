# *********************************************************
# a_mgrApplication_03/models.py

# *********************************************************
from a_base_02.models import a_base_02, convertClassNameToBaseAndVersion, secDict
from a_library_02 import engine_permissions
from a_mgrApplication_03.models_aux import registeredClassInfo
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.db.models import Sum
from django.forms import ModelForm
from django.forms.util import ValidationError
import cStringIO
import settings
import sys

installedComponentsDict = {}         # ex {'c_comment':'02'}   # key = base component name, value = component version

# *********************************************************
def componentInstalled(compNameWithoutVersion):
    if compNameWithoutVersion in installedComponentsDict:   return installedComponentsDict[compNameWithoutVersion]
    else:                                                   return False

# *********************************************************
def addComponent(compNameWithoutVersion, version):
    installedComponentsDict[compNameWithoutVersion] = version

# *********************************************************
def removeComponent(compNameWithoutVersion):
    del installedComponentsDict[compNameWithoutVersion]

# *********************************************************
class a_mgrApplication_03(a_base_02):
    name              = models.CharField        (max_length = 100)
    name_plural       = models.CharField        (max_length = 100)
    basename          = models.CharField        (max_length = 100, help_text="ex: v_problems")
    homeview          = models.CharField        (max_length = 100, help_text="ex: v_problems_01_VIEW_List")
    comment           = models.TextField        ()
    released          = models.BooleanField     (default=False)    
    auto_fields       = ['auto_timeStamp', 'auto_citizen', 'auto_createdTimeStamp', 'auto_createdBy', 'auto_tags'] 
    
    # -----------------------------------------------------
    def entryInit_c_nav_02_menu(cls):
        menuDict = []  
###        menuDict.append({
###                            'displayText'                           :   'Applications',
###                            'menu'                                  :   'SIDE',
###                            'view'                                  :   'a_mgrApplication_03_VIEW_List',
###                            'priority'                              :   9,
###                            'isLocal'                               :   False,
###                            'parentViewList'                        :   [],
###                            'required_viewParamsList'               :   [],
###                            'altSelectOnViewList'                   :   [],
###                            'renderMethod'                          :   '',
###                            'criteriaMethod'                        :   '',
###                       })  
        menuDict.append({
                            'displayText'                           :   'Add Application',
                            'menu'                                  :   'SIDE_LOCAL',
                            'view'                                  :   'a_mgrApplication_03_VIEW_Add',
                            'priority'                              :   2,
                            'isLocal'                               :   True,
                            'parentViewList'                        :   ['a_mgrApplication_03_VIEW_List'],
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   '',
                            'renderMethod'                          :   '',
                            'criteriaMethod'                        :   '',
                       })  
        return menuDict 
    entryInit_c_nav_02_menu = classmethod(entryInit_c_nav_02_menu)      

    # -----------------------------------------------------
    def viewSecurityLookupMethod(viewName):
        from a_base_02.models import secDict
        local_ViewDict = {}
#        local_ViewDict['a_mgrApplication_03_VIEW_List']            = secDict['s_guest']
#        local_ViewDict['a_mgrApplication_03_VIEW_Detail']          = secDict['s_guest']
#        local_ViewDict['a_mgrApplication_03_VIEW_Add']             = secDict['s_developer']
#        local_ViewDict['a_mgrApplication_03_VIEW_Edit']            = secDict['s_developer']
#        local_ViewDict['a_mgrApplication_03_VIEW_Delete']          = secDict['s_developer']
#        local_ViewDict['a_mgrApplication_03_VIEW_subscribetoggle'] = secDict['s_citizen']
        local_ViewDict['a_mgrApplication_03_VIEW_List']                             = secDict['s_developer']
        local_ViewDict['a_mgrApplication_03_VIEW_Detail']                           = secDict['s_developer']
        local_ViewDict['a_mgrApplication_03_VIEW_Add']                              = secDict['s_developer']
        local_ViewDict['a_mgrApplication_03_VIEW_Edit']                             = secDict['s_developer']
        local_ViewDict['a_mgrApplication_03_VIEW_Delete']                           = secDict['s_developer']
        local_ViewDict['a_mgrApplication_03_VIEW_subscribetoggle']                  = secDict['s_developer']
        local_ViewDict['a_mgrApplication_03_VIEW_genericUserAppSubscriptionToggle'] = secDict['s_citizen']
        local_ViewDict['a_mgrApplication_03_VIEW_genericUserAppVote']               = secDict['s_citizen']
        
        if viewName not in local_ViewDict: return secDict['s_undefined']
        else:                              return local_ViewDict[viewName]  
    viewSecurityLookupMethod = staticmethod(viewSecurityLookupMethod)     
     
    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.name)
    def get_absolute_url(self):     return "/a_mgrApplication_03/%i/" % self.id
    def delete(self, **kwargs):     super(a_mgrApplication_03, self).delete(**kwargs)
    def save(self, **kwargs):       super(a_mgrApplication_03, self).save(**kwargs)       

    # -----------------------------------------------------
    def entryInit_class(cls):
        from a_mgrApplication_03.models_aux import registeredClassInfo        
        errorList          = []
        dependancyDict     = {}

        alwaysRequiredList = [
                                'a_base_02', 
                                'a_citizen_02',
#                                'a_friends_01',
                                'a_library_02',
#                                'a_geoAddress_01',
#                                'a_googleMap_01',
                                'a_mgrCache_01',
#                                'a_mdMigration_01',
                                'a_mgrApplication_03',
                                'a_mgrCategories_02',
                                'a_mgrEmail_02',
                                'a_msgSocial_02',
                                'a_msgUser_02',
#                                'a_mgrPublish_02',
                                'a_mgrSidebar_02',
                                'a_mgrVerHistory_01',
                                'a_update_02',
#                                'a_discussion_01',
                             ]

        for x in settings.INSTALLED_APPS:
            if x[:6] <> 'django': # skip the django installed apps
                knownComponent = True
                
                # Verify always required components are present
                if x[:2] == 'a_':
                    if x not in alwaysRequiredList:
                        errorList.append('module not in alwaysRequiredList: %s' % (x))
                # Gather dependencies for other components
                elif x[:2] in ['c_', 'd_', 'e_', 'v_', 'w_', 'p_', 'ev']:
                    convertedDict = convertClassNameToBaseAndVersion(x)
                    addComponent(convertedDict['baseName'], convertedDict['version'])
                    
###                    dependencyList = registeredClassInfo.get_classObject_fromBaseName(convertedDict['baseName']).entryInit_dependencies()
###                    if x not in dependancyDict:
###                        dependancyDict[x] = []
###                        for y in dependencyList:
###                            dependancyDict[x].append(y)
###                    else:
###                        errorList.append('module %s already found in dependencyDict' % (x))
                else:
                    if x == 'tagging' or x == 'compress': # small hack to allow the django tagging and compress modules I just started to use.
                        pass
                    else:
                        knownComponent = False
                        errorList.append('unknown module type (%s): %s' % (x[:2], x))

        # Verify dependencies are satisfied 
        for k, v in dependancyDict.items():
            for x in v:
                if x not in settings.INSTALLED_APPS:
                    errorList.append('component %s dependency %s not found' % (k, x))
                    
        if errorList:
            errorList.insert(0, "a_mgrApplication_03.entryInit_class")
            errorString = '\n*** '.join(errorList)
            raise Exception, errorString        
        
    entryInit_class = classmethod(entryInit_class) 
    
    # -----------------------------------------------------
    # I THINK THIS MW CALL NEEDS TO BE DONE FOR ALL CALLS AND NOT JUST IF IT IS A VIEW
    def mw_request_multiHost(request):
        try:
            # get host stripping of the port number if there
            host = (request.META["HTTP_HOST"]).split(':',1)[0]
            request.urlconf = settings.HOST_MIDDLEWARE_URLCONF_MAP[host]
        except KeyError:
            pass 
#        return None
    mw_request_multiHost = staticmethod(mw_request_multiHost)  

    # -----------------------------------------------------
    def mw_request_WEBSITE_IS_DOWN(request):
        if settings.WEBSITE_IS_DOWN:
            request.META['WEBSITE_IS_DOWN'] = True
    mw_request_WEBSITE_IS_DOWN = staticmethod(mw_request_WEBSITE_IS_DOWN)      
    
    # -----------------------------------------------------
    # I THINK THIS MW CALL NEEDS TO BE DONE FOR ALL CALLS AND NOT JUST IF IT IS A VIEW
    def mw_response_multiHost(request, response):
        if getattr(request, "urlconf", None):
            from django.utils.cache import patch_vary_headers            
            patch_vary_headers(response, ('Host',))        
        return response
    mw_response_multiHost = staticmethod(mw_response_multiHost)    
    
    # -----------------------------------------------------
    def mw_request_duoUsage(request):
        from a_citizen_02.models import a_citizen_02
        if request.META['HTTP_HOST'] == settings.FACEBOOK_HTTP_HOST:
            request.META['duo_Usage']                   = 'FACEBOOK'
            request.META['duo_mapHost']                 = settings.DIRECT_HTTP_HOST
            request.META['duo_Direct']                  = False
            request.META['duo_FormActionPrepend']       = 'http://apps.new.facebook.com'        # 'http://apps.facebook.com'
            request.META['duo_citizen']                 = a_citizen_02.getCurrentFromFacebook(request)
            
            # If 'duo_citizen' returned isnt an instance of a_citizen_02 then getCurrentFromFacebook failed.
            # Probably because the current FB user isn't logged in and hasn't given access to the application.
            # In that case redirect them to the output returned from getCurrentFromFacebook as this is the
            # standard facebook login url for this app
            if not isinstance(request.META['duo_citizen'], a_citizen_02):
                return request.META['duo_citizen']
        
            # Force language to Facebook users preference
            if 'fb_sig_locale' in request.POST:
                from django.utils import translation
                translation.activate(request.POST['fb_sig_locale'])
                request.LANGUAGE_CODE = translation.get_language()
        
        elif request.META['HTTP_HOST'] == settings.DIRECT_HTTP_HOST or request.META['HTTP_HOST'] == settings.DIRECT_HTTP_HOST[4:]:
            request.META['duo_Usage']                 = 'DIRECT'
            request.META['duo_mapHost']               = request.META['HTTP_HOST']
            request.META['duo_Direct']                = True
            request.META['duo_FormActionPrepend']     = 'http://'+request.META['HTTP_HOST']
            request.META['duo_citizen']               = a_citizen_02.getCurrentFromDirect(request)
#            print "*** request.META['duo_citizen'] = %s" % (request.META['duo_citizen'])
        else:
            contextDict = {}
            outString = "Unknown request.META['HTTP_HOST'] = (%s), settings.DIRECT_HTTP_HOST = (%s)"  % (request.META['HTTP_HOST'], settings.DIRECT_HTTP_HOST)
            contextDict['main_1'] = outString

            # rest is a hack to allow this to continue gracefully. previously to this it would error out into an Apache error which
            # really didn't help find the problem.
            from a_base_02.models import secDict
            request.META['citizen_rights']            = secDict['s_guest']
            request.META['duo_Usage']                 = 'DIRECT'
            request.META['duo_mapHost']               = request.META['HTTP_HOST']
            request.META['duo_Direct']                = True
            request.META['duo_FormActionPrepend']     = 'http://'+request.META['HTTP_HOST']
            request.META['duo_citizen']               = a_citizen_02.getCurrentFromDirect(request)
        
            return a_base_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')   
        
        engine_permissions.setUserPermissions(request)
   
        return None
    mw_request_duoUsage = staticmethod(mw_request_duoUsage)  

    # -----------------------------------------------------
    def mw_view_applicationDetails(request, view_func, view_args, view_kwargs):
        request.META['VERSION_MAJOR'] = settings.VERSION_MAJOR
        request.META['VERSION_MINOR'] = "%s%s" % (settings.VERSION_MINOR_1, settings.VERSION_MINOR_2)
        request.META['MEDIA_PRJ']     = settings.MEDIA_PRJ
        request.META['MEDIA_LIB']     = settings.MEDIA_LIB

        request.META['VIEW_KWARGS']   = view_kwargs
        
        splitList = (view_func.func_globals['__name__']).split('.',2)
        currentApp = splitList[0]
        currentView = view_func.func_name

##        # if we are in a node_ app then get extract currentApp from the url
##        # ex: from /besomeone/node_goal_a/view/view_boycott/ where view_boycott is the actual app 
##        if (currentApp[:5] == "node_") and (currentView[:10] == 'VIEW_Node_'):
##            splitAppFromUrlList = request.META[o_currentApp']     = currentApp

        request.META['auto_currentApp']             = currentApp
        request.META['auto_currentView']            = currentView
        convertedDict = convertClassNameToBaseAndVersion(request.META['auto_currentApp'])
        request.META['auto_currentApp_baseName']    = convertedDict['baseName']
        request.META['auto_currentApp_version']     = convertedDict['version']
        
        
##        print "request.META['auto_currentApp']             = %s" % (request.META['auto_currentApp'])
##        print "request.META['auto_currentView']            = %s" % (request.META['auto_currentView'])
##        print "request.META['auto_currentApp_baseName']    = %s" % (request.META['auto_currentApp_baseName'])
##        print "request.META['auto_currentApp_version']     = %s" % (request.META['auto_currentApp_version'])
        
        # default value - over riden by specific problems
        request.META['problem_banner'] = {'file': 'http://%s/%s/images/besomeone-text-transparent-583x100.png' % (request.META['duo_mapHost'], request.META['MEDIA_PRJ']), 'alt': 'be someone'}

        # set a default title but this should be overwritten in each view
        if request.META['duo_Direct']: 
            a_mgrApplication_03.setTitle(request)

        request.META['baseContext_linkHome']         = reverse(settings.HOME_VIEW, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))
        request.META['RECAPTCHA_PUBLIC_KEY']         = settings.RECAPTCHA_PUBLIC_KEY   

        lastPagination_appName = request.session.get('lastPagination_appName')
        if lastPagination_appName and (lastPagination_appName <> request.META['auto_currentApp']+"_"+request.META['auto_currentView']):
            if '_sort_' in request.session: del request.session['_sort_']
            if '_page_' in request.session: del request.session['_page_']

        return None    
    mw_view_applicationDetails = staticmethod(mw_view_applicationDetails) 
    
    # -----------------------------------------------------
    def mw_request_citizenDetails(request):
#        from a_friends_01.models import a_friends_01
        from a_msgUser_02.models import a_msgUser_02        
        from e_thread_03.models import e_thread_replyTracking_03
##        from c_comment_03.models import c_comment_03_replyTracking_03
        request.META['friendsIDlist'] = [] 
        
##        if request.META['duo_citizen']:
##            QS = a_friends_01.objects.filter(citizen=request.META['duo_citizen'])
##            for x in QS:
##                request.META['friendsIDlist'].append(x.friend.id)
            
        return None    
    mw_request_citizenDetails = staticmethod(mw_request_citizenDetails) 
    
    # -----------------------------------------------------
    def mw_request_devModeKeyCheck(request):
        devMode = False
        
        # check for ?devMode url key and toggle displayProfile session display value
        if request.REQUEST.has_key('devMode'):
            if request.session.get('devMode'): request.session['devMode'] = False
            else:                              request.session['devMode'] = True

        # Check displayProfile to see if we should be displaying the profile        
        if request.session.get('devMode'): devMode = True 
        else:                              devMode = False   
        
        if devMode and request.META['duo_citizen'] and ((request.META['duo_citizen'].direct and request.META['duo_citizen'].id == settings.DEV_DIRECT_UID) or (request.META['duo_citizen'].facebook == settings.DEV_FB_UID or request.META['duo_citizen'].facebook == settings.DEV_RaSun_FB_UID)):
            request.META['citizen_rights'] = secDict['s_developer']
#        return None
    mw_request_devModeKeyCheck = staticmethod(mw_request_devModeKeyCheck)
    
    # -----------------------------------------------------
    def mw_view_checkViewSecurity(request, view_func, view_args, view_kwargs):
        if view_func.func_name <> settings.HOME_VIEW:
            
            # Hack to allow admin view for django-eve development
#            if view_func.func_name <> 'root':
            if view_func.func_name <> 'root' and view_func.func_name <> 'doc_index':
                if not engine_permissions.checkUserPermissions(request.META['citizen_rights'], view_func.func_name, view_args, view_kwargs, request):
                    print "*** mw_view_checkViewSecurity: user does not have rights for %s" % (view_func.func_name)
                    return a_base_02.redirectView(request, settings.HOME_VIEW, 'user_no')
                else:
                    return None
        else:
            return None
        return None
    mw_view_checkViewSecurity = staticmethod(mw_view_checkViewSecurity)         
    
    # -----------------------------------------------------
    def mw_request_printCapture(request):
        request.savedOut = sys.stdout
        sys.stdout = cStringIO.StringIO()        
        return None
    mw_request_printCapture = staticmethod(mw_request_printCapture)
    
    # -----------------------------------------------------
    def mw_response_printCapture(request, response):
        if getattr(request, "savedOut", None):
            pStrings = sys.stdout.getvalue()
            sys.stdout.close()
            sys.stdout = getattr(request, "savedOut")
            sys.stdout.write(pStrings)     
                               
#            if response and response.content and pStrings:
#                response.content += "<pre>" + pStrings + "</pre>"  # append profile results to the bottom of page
            
        return response
    mw_response_printCapture = staticmethod(mw_response_printCapture)    
    
    # -----------------------------------------------------
    def mw_view_developerAdmin(request, view_func, view_args, view_kwargs):
        from a_citizen_02.models import a_citizen_02
        
        if (request.META['citizen_rights'] == secDict['s_developer']):
            request.META['devAdmin_citizenAuthorizationsPending']   = a_citizen_02.getAuthorizationsPending(request)
        return None
    mw_view_developerAdmin = staticmethod(mw_view_developerAdmin)         
    
    # -----------------------------------------------------
    def mw_response_stripSpaces(request, response):
        from django.utils.html import strip_spaces_between_tags as short
        
        if 'text/html' in response['Content-Type']: 
            response.content = short(response.content) 
            return response

    mw_response_stripSpaces = staticmethod(mw_response_stripSpaces) 
    
    # -----------------------------------------------------
    def mw_request_trackViewHistory(request):
        
        # get viewHistory from session or a list containing current PATH_INFO
        viewHistory = request.session.get('viewHistory', [request.META['PATH_INFO']])
        
        # insert at beginning new PATH_INFO if unique
        if viewHistory[0] <> request.META['PATH_INFO']:
            viewHistory.insert(0, request.META['PATH_INFO'])

        # put this back into session but keep only a small number
        request.session['viewHistory'] = viewHistory[:settings.MAXIMUM_VIEW_HISTORY]
        
###        print "***************************"
###        for view in viewHistory[:settings.MAXIMUM_VIEW_HISTORY]:
###            print "*** %s" % (view)
        
    mw_request_trackViewHistory = staticmethod(mw_request_trackViewHistory)
    
    # -----------------------------------------------------
    def entryInit_middlewareMethods(cls):
        mw_methods = []

        mw_methods.append([1, 'request',       'mw_request_WEBSITE_IS_DOWN'])
                
        # MultiHost methods if necessary
        if settings.HOST_MIDDLEWARE_URLCONF_MAP:
            mw_methods.append([10, 'request',       'mw_request_multiHost'])
            mw_methods.append([10, 'response',      'mw_response_multiHost'])
            
        # DuoUsage method if necessary
        if settings.FACEBOOK_HTTP_HOST:
            mw_methods.append([20, 'request',       'mw_request_duoUsage'])

        # Generic methods
        mw_methods.append([10, 'view',              'mw_view_applicationDetails'])
        mw_methods.append([30, 'request',           'mw_request_citizenDetails'])
        mw_methods.append([40, 'request',           'mw_request_devModeKeyCheck'])
        mw_methods.append([20, 'view',              'mw_view_checkViewSecurity'])
        mw_methods.append([30, 'view',              'mw_view_developerAdmin'])
        mw_methods.append([79, 'request',           'mw_request_trackViewHistory'])
        
        if settings.DEBUG:
            mw_methods.append([80, 'request',           'mw_request_printCapture'])
            mw_methods.append([80, 'response',          'mw_response_printCapture'])
        else:
            mw_methods.append([90, 'response',          'mw_response_stripSpaces'])
            
        return mw_methods 
    entryInit_middlewareMethods = classmethod(entryInit_middlewareMethods)    
    
        
# *********************************************************
class Form_a_mgrApplication_03(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_mgrApplication_03, self).__init__(*args, **kwargs)
        
        # Common width in characters for all TextInput
        TextInputSize  = 67     
        
        fieldName = 'name'
        self.fields[fieldName].widget = forms.TextInput(attrs={'size':TextInputSize,'maxlength':self.fields[fieldName].max_length})
        fieldName = 'name_plural'
        self.fields[fieldName].widget = forms.TextInput(attrs={'size':TextInputSize,'maxlength':self.fields[fieldName].max_length})
        fieldName = 'basename'
        self.fields[fieldName].widget = forms.TextInput(attrs={'size':TextInputSize,'maxlength':self.fields[fieldName].max_length})
        fieldName = 'homeview'
        self.fields[fieldName].widget = forms.TextInput(attrs={'size':TextInputSize,'maxlength':self.fields[fieldName].max_length})                
        fieldName = 'comment'
        self.fields[fieldName].widget = forms.Textarea(attrs={'cols':'50','rows':'6',})

    # -----------------------------------------------------
    def clean(self):
        error_list = []
        
        if 'basename' in self.cleaned_data:
            try:
                classObj = registeredClassInfo.get_classObject_fromBaseName(self.cleaned_data['basename'])
            except KeyError:
                error_list.append("basename %s not found in registeredClassInfo" % (self.cleaned_data['basename'])) 
            
        if 'homeview' in self.cleaned_data:
            try:
                url = reverse(self.cleaned_data['homeview'])
            except NoReverseMatch:
                error_list.append("reverse for homeview %s not found" % (self.cleaned_data['homeview'])) 
        
        if error_list: raise ValidationError(error_list)
        return self.cleaned_data         

    # -----------------------------------------------------
    class Meta:
        model = a_mgrApplication_03
        fields = (
                    'name',
                    'name_plural',
                    'basename',
                    'homeview',
                    'comment',
                    'released',
                 )    

# *********************************************************
class subscription_01(a_base_02):
    application = models.ForeignKey         (a_mgrApplication_03)
    auto_fields = ['auto_timeStamp','auto_citizen'] 

    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.application)
    def delete(self, **kwargs):     super(subscription_01, self).delete(**kwargs)
    def save(self, **kwargs):       super(subscription_01, self).save(**kwargs)       
    

# *********************************************************
class genericUserAppSubscription(a_base_02):
    auto_fields       = ['auto_timeStamp', 'auto_citizen','auto_content_object']     

# *********************************************************
class genericUserAppVote(a_base_02):
    mode              = models.CharField        (max_length = 20)
    vote              = models.IntegerField     (default=0)
    auto_fields       = ['auto_timeStamp', 'auto_citizen','auto_content_object']     
    
    # -----------------------------------------------------
    def delete(self, **kwargs):
        auto_content_object = self.auto_content_object
        mode                = self.mode  
        super(genericUserAppVote, self).delete(**kwargs)
        genericUserAppVoteTotal.updateTotal(kwargs['request'], auto_content_object, mode)

    # -----------------------------------------------------
    def save(self, **kwargs):       
        super(genericUserAppVote, self).save(**kwargs)      
        genericUserAppVoteTotal.updateTotal(kwargs['request'], self.auto_content_object, self.mode)

# *********************************************************
class genericUserAppVoteTotal(a_base_02):
    mode              = models.CharField        (max_length = 20)
    total             = models.IntegerField     (default=0)
    auto_fields       = ['auto_content_object']     
    
    # -----------------------------------------------------
    def updateTotal(request, auto_content_object, mode):
        
        auto_content_type = ContentType.objects.get_for_model(auto_content_object)
        
        currentTotal = genericUserAppVote.objects.filter(
                                                       auto_object_id__exact        = auto_content_object.id,
                                                       auto_content_type__exact     = auto_content_type,
                                                       mode__exact                  = mode,
                                                       ).aggregate(Sum('vote'))
        try:
            totalInstance = genericUserAppVoteTotal.objects.get(
                                                           auto_object_id__exact        = auto_content_object.id,
                                                           auto_content_type__exact     = auto_content_type,
                                                           mode__exact                  = mode,
                                                     )
        except ObjectDoesNotExist:          
            totalInstance                       = genericUserAppVoteTotal()
            totalInstance.auto_content_object   = auto_content_object
            totalInstance.mode                  = mode
        
        totalInstance.total = currentTotal['vote__sum']
        totalInstance.save(request=request)
    updateTotal = staticmethod(updateTotal)    

























