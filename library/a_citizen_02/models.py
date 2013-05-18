# *********************************************************
# a_citizen_02/models.py

# *********************************************************
from a_base_02.models import a_base_02
from django import forms
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm
from django.forms.util import ValidationError
from facebook.djangofb import get_facebook_client
from recaptcha.client import captcha
import facebook.djangofb as facebook2
import random
import settings
import time

# *********************************************************
def validate_passwords(pass1, pass2):
    validation_errorList = []
    
    if pass1 <> pass2: 
        validation_errorList.append("passwords must be the same")
    
    if len(pass1) < settings.MIN_PASSWORD_LENGTH or len(pass2) < settings.MIN_PASSWORD_LENGTH:
        validation_errorList.append("passwords must be at least %s digits long" % (settings.MIN_PASSWORD_LENGTH))
    
    return validation_errorList     

# *********************************************************
def validate_email(emailAddress):
    validation_errorList = []
    
    # Test email address is unique
    QS = User.objects.filter(email__exact=emailAddress)
    if QS.count(): validation_errorList.append("email address '%s' is already in use" % (emailAddress))
    return validation_errorList     
        
# *********************************************************
class a_citizen_02(a_base_02):
    direct                    = models.ForeignKey       (User, related_name='directCitizen', blank=True, null=True)
    facebook                  = models.IntegerField     (default=0)
    name                      = models.CharField        (max_length=60)  # set during appropriate getCurrent call
    directEmailValidated      = models.BooleanField     (default=False)
    authenticated             = models.IntegerField     (default=0)
    authenticated_count       = models.IntegerField     (default=0)
    reasonJoined              = models.TextField        (verbose_name = 'Reason for Joining') 
    auto_fields               = ['auto_timeStamp', 'auto_createdTimeStamp']
    
    # -----------------------------------------------------
    def entryInit_c_nav_02_menu(cls):
        menuDict = []  
        menuDict.append({
                            'displayText'                           :   'citizen',
                            'menu'                                  :   'SIDE',
                            'view'                                  :   'a_citizen_02_VIEW_List',
                            'priority'                              :   3,
                            'isLocal'                               :   False,
                            'parentViewList'                        :   [],
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   [],
                            'renderMethod'                          :   '',
                            'criteriaMethod'                        :   '',
                       })  
        menuDict.append({
                            'displayText'                           :   'login form',
                            'menu'                                  :   'RIGHTCOL',                            
                            'view'                                  :   'a_urlPassChange_02_VIEW_changeRequest',
                            'priority'                              :   1,
                            'isLocal'                               :   False,
                            'parentViewList'                        :   [],
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   [],
                            'renderMethod'                          :   'loginForm',
                            'criteriaMethod'                        :   'userIsGuest',
                       })  
###        menuDict.append({
###                            'displayText'                           :   'join',
###                            'menu'                                  :   'CITIZEN',
###                            'view'                                  :   'a_citizen_02_VIEW_Register',
###                            'priority'                              :   2,
###                            'isLocal'                               :   False,
###                            'parentViewList'                        :   [],
###                            'required_viewParamsList'               :   [],
###                            'altSelectOnViewList'                   :   [],
###                            'renderMethod'                          :   '',
###                            'criteriaMethod'                        :   'userIsGuest',
###                       })  
###        menuDict.append({
###                            'displayText'                           :   'recover password',
###                            'menu'                                  :   'CITIZEN',
###                            'view'                                  :   'a_urlPassChange_02_VIEW_changeRequest',
###                            'priority'                              :   3,
###                            'isLocal'                               :   False,
###                            'parentViewList'                        :   [],
###                            'required_viewParamsList'               :   [],
###                            'altSelectOnViewList'                   :   [],
###                            'renderMethod'                          :   '',
###                            'criteriaMethod'                        :   'userIsGuest',
###                       })  
######        menuDict.append({
######                            'displayText'                           :   'citizen',
######                            'menu'                                  :   'CITIZEN',
######                            'view'                                  :   'd_premises_02_VIEW_home',
######                            'priority'                              :   5,
######                            'isLocal'                               :   False,
######                            'parentViewList'                        :   [],
######                            'required_viewParamsList'               :   [],
######                            'altSelectOnViewList'                   :   [],
######                            'renderMethod'                          :   'citizenLinkRender',
######                            'criteriaMethod'                        :   'userIsCitizen',
######                       })  
##        menuDict.append({
##                            'displayText'                           :   'prefs',
##                            'menu'                                  :   'CITIZEN',
##                            'view'                                  :   'a_citizen_02_VIEW_Preferences',
##                            'priority'                              :   10,
##                            'isLocal'                               :   False,
##                            'parentViewList'                        :   [],
##                            'required_viewParamsList'               :   [],
##                            'altSelectOnViewList'                   :   ['a_citizen_02_VIEW_PreferencesEditEmail','a_citizen_02_VIEW_PreferencesEditPassword'],
##                            'renderMethod'                          :   '',
##                            'criteriaMethod'                        :   'userIsCitizen',
##                       })  
        menuDict.append({
                            'displayText'                           :   'logout',
#                            'menu'                                  :   'CITIZEN',
#                            'menu'                                  :   'RIGHTCOL',                            
                            'menu'                                  :   'SIDE',                            
                            'view'                                  :   'a_citizen_02_VIEW_Logout',
                            'priority'                              :   11,
                            'isLocal'                               :   False,
                            'parentViewList'                        :   [],
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   [],
                            'renderMethod'                          :   '',
                            'criteriaMethod'                        :   'userIsCitizen',
                       })  
        return menuDict 
    entryInit_c_nav_02_menu = classmethod(entryInit_c_nav_02_menu)      
    
    # -----------------------------------------------------
    def citizenLinkRender(request, view_func, view_args, view_kwargs):
#        if request.META['auto_currentView'] == 'a_citizen_02_VIEW_Detail':
#            returnString = "<a href='%s' class='on'>%s</a>(%s)" % (reverse('a_citizen_02_VIEW_Detail', kwargs = {'object_id':request.META['duo_citizen'].id}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), request.META['duo_citizen'].name, request.META['citizen_rights']['name'])
#        else:
#            returnString = "<a href='%s'>%s</a> (%s)" % (reverse('a_citizen_02_VIEW_Detail', kwargs = {'object_id':request.META['duo_citizen'].id}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), request.META['duo_citizen'].name, request.META['citizen_rights']['name'])
#        return returnString

        returnString = "%s (%s)&nbsp;" % (request.META['duo_citizen'].name, request.META['citizen_rights']['name'])
        return returnString
    citizenLinkRender = staticmethod(citizenLinkRender)   
     
    # -----------------------------------------------------
    def loginForm(request, view_func, view_args, view_kwargs):
        loginContextDict = {}
        formClass = Form_engine_menu_a_Login
        form_action = request.META['duo_FormActionPrepend'] + request.META['PATH_INFO']

        resultDict = a_citizen_02.processForm_01(request, formClass, None, 'a_citizen_02/templates/FORM_Login.html', resetFormOnSuccess=True, form_action=form_action)
        if resultDict['success']:
            # make sure the user exists
            user = authenticate(username=resultDict['cleanData']['username'], password=resultDict['cleanData']['password'])        
            if user is not None:
                if user.is_active:
                    from a_library_02 import engine_permissions
                    from a_mgrApplication_03.models import a_mgrApplication_03
                    
                    # log them in
                    login(request, user)
                    request.META['duo_citizen'] = a_citizen_02.getCurrentFromDirect(request)
                    engine_permissions.setUserPermissions(request)
                    a_mgrApplication_03.mw_request_citizenDetails(request)
                    
                    formResultDict = {'redirect':True, 'display':'dislay BLOCK_LoggedIn'}
                else:
                    # generate error if that user account is no longer active
                    error_message = "Your account has been disabled!"
                    formResultDict = {'redirect':False,'display':resultDict['out'],'error':error_message}
            else:
                # generate error if the user could not be logged in
                error_message = "Your username or password was incorrect."
                formResultDict = {'redirect':False,'display':resultDict['out'],'error':error_message}
        else: 
            error_message = ""
            formResultDict = {'redirect':False,'display':resultDict['out'],'error':error_message}    
        
        if not formResultDict['redirect']:
            loginContextDict['form_itself'] = formResultDict['display']
            loginContextDict['form_errors'] = formResultDict['error']
            return a_citizen_02.processTemplate_01(request, 'a_citizen_02/templates/BLOCK_LogIn.html', loginContextDict)
        else:
            return ' '
    loginForm = staticmethod(loginForm)    
    
    # -----------------------------------------------------
    def viewSecurityLookupMethod(viewName):
        from a_base_02.models import secDict
        local_ViewDict = {}
        local_ViewDict['a_citizen_02_VIEW_List']                         = secDict['s_developer']
        local_ViewDict['a_citizen_02_VIEW_Detail']                       = secDict['s_guest']
        local_ViewDict['a_citizen_02_VIEW_Register']                     = secDict['s_guest']
        local_ViewDict['a_citizen_02_VIEW_Welcome']                      = secDict['s_guest']
        local_ViewDict['a_citizen_02_VIEW_Logout']                       = secDict['s_denied']
        local_ViewDict['a_citizen_02_VIEW_Authenticate']                 = secDict['s_developer']
        local_ViewDict['a_citizen_02_VIEW_Edit']                         = secDict['s_developer']
        local_ViewDict['a_urlPassChange_02_VIEW_List']                   = secDict['s_developer']
        local_ViewDict['a_urlPassChange_02_VIEW_validateEmail']          = secDict['s_guest']
        local_ViewDict['a_urlPassChange_02_VIEW_changeRequest']          = secDict['s_guest']
        local_ViewDict['a_urlPassChange_02_VIEW_changeRequestSent']      = secDict['s_guest']        
        
        local_ViewDict['a_citizen_02_VIEW_Preferences']                  = secDict['s_denied']
        local_ViewDict['a_citizen_02_VIEW_PreferencesEditPassword']      = secDict['s_citPending']
        local_ViewDict['a_citizen_02_VIEW_PreferencesEditEmail']         = secDict['s_citPending']
        local_ViewDict['a_citizen_02_VIEW_AnotherEmailValidation']       = secDict['s_citPending']
        local_ViewDict['a_citizen_02_VIEW_AnotherAuthorization']         = secDict['s_denied']
        
        if viewName not in local_ViewDict: return secDict['s_undefined']
        else:                              return local_ViewDict[viewName]  
    viewSecurityLookupMethod = staticmethod(viewSecurityLookupMethod)    

    # -----------------------------------------------------
    def __unicode__(self):          return self.name
    def get_absolute_url(self):     return "/a_citizen_02/%i/" % self.id
    def delete(self, **kwargs):     super(a_citizen_02, self).delete(**kwargs)
    def save(self, **kwargs):
        super(a_citizen_02, self).save(**kwargs)   
        
###        # create an engine_citizenPrefs_a instance if it doesn't already exist.
###        try:
###            prefs = self.engine_citizenprefs_a
###        except ObjectDoesNotExist:
###            from engine_citizenPrefs_a.models import engine_citizenPrefs_a
###            prefInst = engine_citizenPrefs_a(citizen=self)
###            prefInst.save()
    
    # -----------------------------------------------------
    def getAuthorizationsPending(request):
        from django.db.models import Q
        returnString = ''
        
        QS = a_citizen_02.objects.filter(Q(authenticated__exact=0, directEmailValidated=True)|Q(facebook__gt=0,authenticated__exact=0))
        if QS.count():
            returnString = "<a href='%s'>%s citizen authorizations pending</a>" % (reverse('a_citizen_02_VIEW_Authenticate', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , QS.count())
        return returnString
    getAuthorizationsPending = staticmethod(getAuthorizationsPending)        
    
    # -----------------------------------------------------
    def generateDirectName(request, user):
        if user:
            fn = user.first_name 
            ln = user.last_name 
        else:    
            fn = request.user.first_name 
            ln = request.user.last_name
        return ''.join([fn," ",ln])
    generateDirectName = staticmethod(generateDirectName)        
    
    # -----------------------------------------------------
    def generateFacebookName(facebookUID):
        return "FB User (id = %s)" % (facebookUID)
    generateFacebookName = staticmethod(generateFacebookName)        
    
    # -----------------------------------------------------
    def birthNewCitizen(request, direct='', facebook='', **kwargs):
        timeNow = time.time()
        random.seed(timeNow)
        
        # Generate id's until find one that isn't used
        randId = settings.DEV_DIRECT_UID
        while 1:
            try:
                QS = a_citizen_02.objects.get(pk=randId)
                randId = int(random.random() * 1000000000)
            except ObjectDoesNotExist:
                break

        if direct:          instance = a_citizen_02.objects.create(id=randId, direct=direct,     name=a_citizen_02.generateDirectName(request, direct), **kwargs)
        elif facebook:      instance = a_citizen_02.objects.create(id=randId, facebook=facebook, name=a_citizen_02.generateFacebookName(facebook, **kwargs))
        return instance
    birthNewCitizen = staticmethod(birthNewCitizen)        

    # -----------------------------------------------------
    def getCurrentFromDirect(request):
        try:
            if request.user.id is None: 
                instance = None        # guests and users not signed in
            else: 
                instance = a_citizen_02.objects.get(direct=request.user)
        except ObjectDoesNotExist:
            try:
                instance = a_citizen_02.objects.get(name=request.user.username)
                instance.direct = request.user
                instance.save(request=request)
            except ObjectDoesNotExist:
                instance = a_citizen_02.birthNewCitizen(request, direct=request.user)
        return instance
    getCurrentFromDirect = staticmethod(getCurrentFromDirect)     
    
###    # -----------------------------------------------------
####    @facebook2.require_login()
###    def getCurrentFromFacebook(request):
###        print "*****************************************************************************"
###        facebook = get_facebook_client()
###        print "*** facebook = %s" % (facebook)
###        print "*** facebook.uid = %s" % (facebook.uid)
###        fb_ID = facebook.uid
###        if not fb_ID: 
###            print "*** request.POST['fb_sig_canvas_user'] = %s" % (request.POST['fb_sig_canvas_user'])
###            fb_ID = request.POST['fb_sig_canvas_user']
###        print "*****************************************************************************"
###        try:
####            instance = a_citizen_02.objects.get(facebook=int(facebook.uid))
###            instance = a_citizen_02.objects.get(facebook=int(fb_ID))
###        except ObjectDoesNotExist:
####            instance = a_citizen_02.birthNewCitizen(request, facebook=int(facebook.uid))
###            instance = a_citizen_02.birthNewCitizen(request, facebook=int(fb_ID))
###        return instance
###    getCurrentFromFacebook = staticmethod(getCurrentFromFacebook)        


##    for key, value in request.POST.items():
##            if key == "fb_sig_user": 
##            elif key == "fb_sig_added": 
##            elif key == "fb_sig_session_key": 
##            elif key == "fb_sig_expires": 
##            elif key == "fb_sig": 
##            elif key == "fb_sig_time": 
##            elif key == "fb_sig_profile_update_time": 
##            elif key == "fb_sig_api_key": 
##            elif key == "fb_sig_friends": 
##            elif key == "fb_sig_locale": 
##            elif key == "fb_sig_position_fix": 
##            elif key == "fb_sig_request_method": 
##            elif key == "fb_sig_in_canvas":
 

    # -----------------------------------------------------
    @facebook2.require_login()
    def getCurrentFromFacebook(request):
        
#        print "-------------------------------------------------------"
        
#        for key, value in request.POST.items():
#            if key[:6] == 'fb_sig':
#                print "*** key = %30s %s" % (key, value)
# ___________________________________________________________
#WITH @facebook2.require_login() and Mike Harley's FB account                
#*** key =                    fb_sig_time 1221400257.7585
#*** key =                   fb_sig_added 1
#*** key =                  fb_sig_locale en_US
#*** key =            fb_sig_position_fix 1
#*** key =         fb_sig_in_new_facebook 1
#*** key =     fb_sig_profile_update_time 1216223143
#*** key =          fb_sig_request_method GET
#*** key =                    fb_sig_user 604651074
#*** key =             fb_sig_session_key 8aa936ee8ef2866e28536889-604651074
#*** key =                 fb_sig_expires 0
#*** key =                         fb_sig 0fa1af2b734578f297ae499f05d918bd
#*** key =                 fb_sig_api_key 97d02134a3c07c35ff98b95d7588ea39
#*** key =                 fb_sig_friends 36814473,505844967,506011582,506064455,510521229,512761178,515024155,516605211,534319185,546685637,552962291,568142492,578590155,578748135,595140810,605123451,608045730,608342049,636435211,642800777,651596873,655895568,657680990,662173766,662484026,665870435,
#*** key =               fb_sig_in_canvas 1
        
# ___________________________________________________________
#WITHOUT @facebook2.require_login() and Mike Harley's FB account                
#*** key =                    fb_sig_time 1221400211.7892
#*** key =                   fb_sig_added 1
#*** key =                  fb_sig_locale en_US
#*** key =            fb_sig_position_fix 1
#*** key =         fb_sig_in_new_facebook 1
#*** key =     fb_sig_profile_update_time 1216223143
#*** key =          fb_sig_request_method GET
#*** key =                    fb_sig_user 604651074
#*** key =             fb_sig_session_key 8aa936ee8ef2866e28536889-604651074
#*** key =                 fb_sig_expires 0
#*** key =                         fb_sig c3b20aca7944e9cf02098161d59e98b7
#*** key =                 fb_sig_api_key 97d02134a3c07c35ff98b95d7588ea39
#*** key =                 fb_sig_friends 36814473,505844967,506011582,506064455,510521229,512761178,515024155,516605211,534319185,546685637,552962291,568142492,578590155,578748135,595140810,605123451,608045730,608342049,636435211,642800777,651596873,655895568,657680990,662173766,662484026,665870435,
#*** key =               fb_sig_in_canvas 1
        
# ___________________________________________________________
#WITH @facebook2.require_login() and RA SUN FB account     
# NOTHING BECAUS HE HASN'T ADDED THE APPLICATION    
# NOTHING BECAUS HE HASN'T ADDED THE APPLICATION    
# NOTHING BECAUS HE HASN'T ADDED THE APPLICATION    
# NOTHING BECAUS HE HASN'T ADDED THE APPLICATION    
        
# ___________________________________________________________
#WITHout @facebook2.require_login() and RA SUN FB account     
#*** key =                    fb_sig_time 1221400397.421
#*** key =                   fb_sig_added 0
#*** key =                  fb_sig_locale en_US
#*** key =            fb_sig_position_fix 1
#*** key =         fb_sig_in_new_facebook 1
#*** key =          fb_sig_request_method GET
#*** key =                         fb_sig 3b34aa11f635cd65a21c06973133c2e2
#*** key =                 fb_sig_api_key 97d02134a3c07c35ff98b95d7588ea39
#*** key =               fb_sig_in_canvas 1     

#        print "*** request.facebook.users.isAppUser() = %s" % (request.facebook.users.isAppUser())  
        
        
#request.facebook.users.getInfo(title=title, body=body)
#            ('uids', list, []),
#            ('fields', list, [('default', ['name'])]),
        

#http://www.facebook.com/login.php?api_key=97d02134a3c07c35ff98b95d7588ea39&v=1.0        
#http://www.facebook.com/login.php?api_key=97d02134a3c07c35ff98b95d7588ea39&v=1.0        
#http://www.facebook.com/login.php?api_key=97d02134a3c07c35ff98b95d7588ea39&v=1.0        
#http://www.facebook.com/login.php?api_key=97d02134a3c07c35ff98b95d7588ea39&v=1.0        
        
        
#        print "-------------------------------------------------------"
        
        facebook = get_facebook_client()
        fbId = facebook.uid
        
#        if not fbId: 
##            fbId = 604651074
#            fbId = 1099808809
        try:
            instance = a_citizen_02.objects.get(facebook=fbId)
        except ObjectDoesNotExist:
#            instance = a_citizen_02.objects.create(facebook=int(facebook.uid), name=a_citizen_02.generateFacebookName((int(facebook.uid))))
            instance = a_citizen_02.birthNewCitizen(request, facebook=fbId)
        return instance
    getCurrentFromFacebook = staticmethod(getCurrentFromFacebook)  

# *********************************************************
class Form_a_citizen_02(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_citizen_02, self).__init__(*args, **kwargs)

        TextInputSize  = 67
        fieldName = 'name'
        self.fields[fieldName] = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':30,}))   
        fieldName = 'authenticated'
        self.fields[fieldName] = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':30,})) 
        fieldName = 'reasonJoined'
        self.fields[fieldName].widget = forms.Textarea(attrs={'cols':'50','rows':'8',})        
        
    # -----------------------------------------------------
    class Meta:
        model = a_citizen_02
        fields = ('name','directEmailValidated','authenticated','reasonJoined',)

# *********************************************************
class Form_a_citizen_02_registerNewUser(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_citizen_02_registerNewUser, self).__init__(*args, **kwargs)
        
        TextInputSize  = 67
        fieldName = 'userName'
        self.fields[fieldName] = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':30,}),       label='User Name', help_text='Must be unique.')                
        fieldName = 'firstName'
        self.fields[fieldName] = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':30,}),       label='First Name')                
        fieldName = 'lastName'
        self.fields[fieldName] = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':30,}),       label='Last Name')                
        fieldName = 'email'
        self.fields[fieldName] = forms.EmailField(max_length=75, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':75,}),       label='Email Address', help_text='Valid address required to validate your registration.')                
        fieldName = 'pass1'
        self.fields[fieldName] = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'size':TextInputSize,'maxlength':128,}), label='Password', help_text="Must be at least %s characters."%(settings.MIN_PASSWORD_LENGTH))                
        fieldName = 'pass2'
        self.fields[fieldName] = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'size':TextInputSize,'maxlength':128}),  label='Password', help_text="Verify pasword.")
        
        fieldName = 'reasonJoined'
#        self.fields[fieldName].widget = forms.Textarea(attrs={'cols':'50','rows':'4',})        
        self.fields[fieldName] = forms.CharField(widget=forms.Textarea(attrs={'cols':'50','rows':'4',}),   label='Reason for Joining', help_text='This website is currently in BETA mode and not fully open to the public. You are welcome to join but accounts must be approved before full participation is granted. Please provide appropriate comments here to help the approval process.')          
        
    # -----------------------------------------------------
    # if exists this is called during success of a form validation and is used to update the instance with
    # additional data the clean or other function might need to continue processing the form validation
    def setInstanceWithExtraRequiredFormValidationValues(self, request):
        self.recaptcha_challenge_field  = request.POST.get("recaptcha_challenge_field")
        self.recaptcha_response_field   = request.POST.get("recaptcha_response_field")
        self.REMOTE_ADDR                = request.META.get("REMOTE_ADDR", None)
        
    # -----------------------------------------------------
    # form clean method to validate all form fields at the same time
    def clean(self):
        error_list = []
       
        # Test userName is unique
        if 'userName' in self.cleaned_data:
            QS = User.objects.filter(username__exact=self.cleaned_data['userName'])
            if QS.count(): error_list.append("username '%s' is already in use" % (self.cleaned_data['userName']))
        
        # Test emailAddress
        if 'email' in self.cleaned_data:
            validaton_errorList = validate_email(self.cleaned_data['email'])
            if validaton_errorList:
                error_list += validaton_errorList            
            
        # Test passwords
        if 'pass1' in self.cleaned_data and 'pass2' in self.cleaned_data:
            validaton_errorList = validate_passwords(self.cleaned_data['pass1'], self.cleaned_data['pass2'])
            if validaton_errorList:
                error_list += validaton_errorList        
    
        # test if captcha is valid
        captcha_response = captcha.submit(self.recaptcha_challenge_field,  
                                          self.recaptcha_response_field,  
                                          settings.RECAPTCHA_PRIVATE_KEY,  
                                          self.REMOTE_ADDR) 
        if not captcha_response.is_valid:  
            error_list.append("incorrect captcha")
        
        if error_list: raise ValidationError(error_list)
        return self.cleaned_data        
        
    # -----------------------------------------------------
    class Meta:
        model = a_citizen_02
        fields = ('userName', 'firstName', 'lastName', 'email', 'pass1', 'pass2','reasonJoined',)         

# *********************************************************
class Form_a_citizen_02_pendingCitizenAuthorizations(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_citizen_02_pendingCitizenAuthorizations, self).__init__(*args, **kwargs)

        fieldName = 'authSelect'
#        self.fields[fieldName] = forms.ChoiceField(required=False, initial='----', choices=(('----', '----'), ('1', 'Authorize'), ('-1', 'Deny'), ('0', 'Decide Later'),), widget=forms.Select(attrs={'onchange':"document.getElementById('Form_a_citizen_02_pendingCitizenAuthorizations_id').submit()"}))             
        self.fields[fieldName] = forms.ChoiceField(required=False, initial='----', choices=(('----', '----'), ('1', 'Authorize'), ('-1', 'Deny'), ('0', 'Decide Later'),))             
        fieldName = 'reasonfordeny'
        self.fields[fieldName] = forms.CharField(required=False, label='Reason for Denying Authorization')
                
    # -----------------------------------------------------
    class Meta:
        model = a_citizen_02
        fields = ('authSelect','reasonfordeny',)
   
# *********************************************************
class Form_a_citizen_02_editPassword(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_citizen_02_editPassword, self).__init__(*args, **kwargs)
        
        TextInputSize  = 67
        fieldName = 'current_password'
        self.fields[fieldName] = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'size':TextInputSize,'maxlength':128,}))                
        fieldName = 'new_pass1'
        self.fields[fieldName] = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'size':TextInputSize,'maxlength':128,}))                
        fieldName = 'new_pass2'
        self.fields[fieldName] = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'size':TextInputSize,'maxlength':128,}))
        
    # -----------------------------------------------------
    # if exists this is called during success of a form validation and is used to update the instance with
    # ith additional data the clean or other function might need to continue processing the form validation
    def setInstanceWithExtraRequiredFormValidationValues(self, request):
        self.citizen = request.META['duo_citizen']
        
    # -----------------------------------------------------
    # form clean method to validate all form fields at the same time
    def clean(self):
        error_list = []
        
        if 'current_password' in self.cleaned_data:
            if not check_password(self.cleaned_data['current_password'], self.citizen.direct.password):
                error_list.append('did not enter correct current password')
       
        # Test new passwords    
        if 'new_pass1' in self.cleaned_data and 'new_pass2' in self.cleaned_data:
            validaton_errorList = validate_passwords(self.cleaned_data['new_pass1'], self.cleaned_data['new_pass2'])
            if validaton_errorList:
                error_list += validaton_errorList
            
        if error_list: raise ValidationError(error_list)
        return self.cleaned_data 
        
    # -----------------------------------------------------
    class Meta:
        model = a_citizen_02
        fields = ('current_password','new_pass1','new_pass2',)
   
# *********************************************************
class Form_a_citizen_02_editEmail(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_citizen_02_editEmail, self).__init__(*args, **kwargs)
        
        TextInputSize  = 67
        fieldName = 'email'
        self.fields[fieldName] = forms.EmailField(max_length=75, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':75,}),       label='Email Address')                        
        
    # -----------------------------------------------------
    # form clean method to validate all form fields at the same time
    def clean(self):
        error_list = []
        
        # Test emailAddress
        if 'email' in self.cleaned_data:
            validaton_errorList = validate_email(self.cleaned_data['email'])
            if validaton_errorList:
                error_list += validaton_errorList
            
        if error_list: raise ValidationError(error_list)
        return self.cleaned_data 
        
    # -----------------------------------------------------
    class Meta:
        model = User
        fields = ('email',)
   
# *********************************************************
class Form_engine_menu_a_Login(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_engine_menu_a_Login, self).__init__(*args, **kwargs)
        
        TextInputSize  = 30             
        fieldName = 'username'
        self.fields[fieldName] = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':30,}))
        fieldName = 'password'
        self.fields[fieldName] = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'size':TextInputSize,'maxlength':128,}))

    class Meta:
        model = a_citizen_02
        fields = ('username','password',)
        
# *********************************************************
class a_urlPassChange_02(a_base_02):
    rand1                = models.IntegerField       (max_length=14, blank=True, null=True)
    rand2                = models.IntegerField       (max_length=14, blank=True, null=True)
    user                 = models.ForeignKey         (User)
    
    auto_fields = ['auto_timeStamp'] 
    
    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.user)
    def get_absolute_url(self):     return "/a_urlPassChange_02/%i/" % self.id
    def delete(self, **kwargs):     super(a_urlPassChange_02, self).delete(**kwargs)
    
    # -----------------------------------------------------
    # non standard save
    def save(self, **kwargs):  
        # Delete any existing instances for this user because "there can be only one"!
        QS = a_urlPassChange_02.objects.filter(user__exact=self.user)
        for x in QS: 
#            x.delete(request=request)            
            x.delete()            
        
        timeNow = time.time()
        random.seed(timeNow)
        self.rand1 = int(random.random() * 100000000)
        self.rand2 = int(random.random() * 100000000) 
        super(a_urlPassChange_02, self).save(**kwargs)   
        
    # -----------------------------------------------------
    def returnValidationUrl(self, request):
        return reverse('a_urlPassChange_02_VIEW_validateEmail', kwargs = {'userId':self.user.id,'rand1':self.rand1,'rand2':self.rand2}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))
    
# *********************************************************
class Form_a_urlPassChange_02_passChange(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_urlPassChange_02_passChange, self).__init__(*args, **kwargs)
        
        TextInputSize  = 67
        fieldName = 'username'
        self.fields[fieldName] = forms.CharField(max_length=75, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':75,}))   
        fieldName = 'email'
        self.fields[fieldName] = forms.CharField(max_length=75, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':75,}))   
        
    # -----------------------------------------------------
    # form clean method to validate all form fields at the same time
    def clean(self):
        error_list = []
        
        if 'username' in self.cleaned_data and 'email' in self.cleaned_data:
            try:
                QS = User.objects.get(username__exact=self.cleaned_data['username'],email__exact=self.cleaned_data['email'])
            except ObjectDoesNotExist:
                error_list.append('Invalid username (%s) or email address (%s)' % (self.cleaned_data['username'], self.cleaned_data['email']))
            if error_list: raise ValidationError(error_list)
        return self.cleaned_data 
        
    # -----------------------------------------------------
    class Meta:
        model = a_urlPassChange_02
        fields = ('username', 'email',)    
        
# *********************************************************
class Form_a_urlPassChange_02_editPassword(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_urlPassChange_02_editPassword, self).__init__(*args, **kwargs)
        
        TextInputSize  = 67
        fieldName = 'new_pass1'
        self.fields[fieldName] = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'size':TextInputSize,'maxlength':128,}))                
        fieldName = 'new_pass2'
        self.fields[fieldName] = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'size':TextInputSize,'maxlength':128,}))
        
    # -----------------------------------------------------
    # form clean method to validate all form fields at the same time
    def clean(self):
        error_list = []
        
        # Test new passwords    
        if 'new_pass1' in self.cleaned_data and 'new_pass2' in self.cleaned_data:
            validaton_errorList = validate_passwords(self.cleaned_data['new_pass1'], self.cleaned_data['new_pass2'])
            if validaton_errorList:
                error_list += validaton_errorList
            
        if error_list: raise ValidationError(error_list)
        return self.cleaned_data 
        
    # -----------------------------------------------------
    class Meta:
        model = a_urlPassChange_02
        fields = ('new_pass1','new_pass2',)       
        
# *********************************************************
class Form_a_citizen_02_requestAuthorizationAgain(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_citizen_02_requestAuthorizationAgain, self).__init__(*args, **kwargs)

        TextInputSize  = 67
        fieldName = 'reasonJoined'
        self.fields[fieldName].widget = forms.Textarea(attrs={'cols':'50','rows':'8',})        
        
    # -----------------------------------------------------
    class Meta:
        model = a_citizen_02
        fields = ('reasonJoined',)                 