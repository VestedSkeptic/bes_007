# *********************************************************
# a_citizen_02/views.py

# *********************************************************
from a_base_02.models import secDict
from a_citizen_02.models import a_citizen_02, Form_a_citizen_02, Form_a_citizen_02_registerNewUser, Form_a_citizen_02_pendingCitizenAuthorizations, Form_a_citizen_02_editPassword, Form_a_citizen_02_editEmail, a_urlPassChange_02, Form_a_urlPassChange_02_passChange, Form_a_urlPassChange_02_editPassword, Form_a_citizen_02_requestAuthorizationAgain #, Form_engine_menu_a_Login
#from a_friends_01.models import a_friends_externalRequest_01
from a_mgrEmail_02.models import a_mgrEmailValidate_02
from a_msgUser_02.models import a_msgUser_02
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.http import Http404
###from e_entry_03.models import e_entry_03
import settings

# *********************************************************
def a_citizen_02_VIEW_Detail(request, object_id):     
    return a_citizen_02.auto_detail(request, object_id, vTitle = 'Citizen Information')

# *********************************************************
def a_citizen_02_VIEW_List(request):
    QS = a_citizen_02.objects.all()
    return a_citizen_02.auto_list(request, QS)

# *********************************************************
def a_citizen_02_VIEW_Edit(request, object_id):
    fn_dict = {'success' : Edit_processSuccess}
    return a_citizen_02.auto_addEdit(request, Form_a_citizen_02, fn_dict, object_id, successRedirectUrlName='a_citizen_02_VIEW_List')

# *********************************************************
def Edit_processSuccess(*args):
    # args[0] = i (the instance)
    # args[1] = request
    # args[2] = cleanDataDict
    # args[3] = redirectReason ('edit' or 'add')   
    args[0].save() 
    
# *********************************************************
def a_citizen_02_VIEW_Logout(request):
    logout(request)
    return a_citizen_02.redirectView(request, settings.HOME_VIEW, 'logout')

# *********************************************************
def a_citizen_02_VIEW_Welcome(request):
    contextDict = {}    
    contextDict['vTitle'] = '&nbsp;'.join(['Welcome to', settings.SITE_NAME, request.META['duo_citizen'].direct.first_name])
    contextDict['main_1'] = a_citizen_02.processTemplate_01(request, 'BLOCK_welcomePage.html')
    
    # also display any e_entry items that are of category welcome in the same manner that about is processed
###    QS = e_entry_03.objects.filter(auto_category__name='welcome').order_by('name')
###    contextDict['main_2'] = a_citizen_02.processTemplate_01(request, 'a_citizen_02/templates/B_welcome.html', {'objectList': QS})   
    
    return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')

# *********************************************************
def a_citizen_02_VIEW_Authenticate(request):
    from django.db.models import Q
    contextDict = {}    
    citizen = ''
    QS = a_citizen_02.objects.filter(Q(authenticated__exact=0, directEmailValidated=True)|Q(facebook__gt=0,authenticated__exact=0))
    if QS.count():
        citizen = QS[0]
        
        fn_dict = {'success' : Authenticate_processSuccess}
        rDict = a_citizen_02.auto_form(
                                          request, 
                                          Form_a_citizen_02_pendingCitizenAuthorizations, 
                                          fn_dict, 
                                          'a_citizen_02_VIEW_Authenticate', 
                                          'F_authenticate.html', 
                                          workObj=citizen,
                                          redirectOnSuccess=True,
                                          )
        if rDict['success']:
            return a_citizen_02.redirectView(request, 'a_citizen_02_VIEW_Authenticate', 'admFormPr')
        else:
            contextDict['vTitle'] = ' '.join(['Authenticate',citizen.name])
            contextDict['main_2'] = rDict['out']
            contextDict['main_1'] = a_citizen_02.processTemplate_01(request, 'BLOCK_Authenticate.html',{'object':citizen})
            return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')
    else:
        contextDict['vTitle'] = 'There are no users waiting authentication.'
        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')

# *********************************************************
def Authenticate_processSuccess(*args):
    # args[0] = i (the instance)
    # args[1] = request
    # args[2] = cleanDataDict
    # args[3] = redirectReason   
    
    args[0].authenticated = args[2]['authSelect']
    args[0].save()
    
    if args[0].authenticated == '1':        
        a_citizen_02.sendUserMessage(args[1], "Your account was authenticated", toCitizen=args[0], type='sys')
        
        # send new citizen an email indicating that their account was authenticated
        subject  = "account authenticated"
        bodyText = a_citizen_02.processTemplate_01(args[1], 'a_citizen_02/templates/E_accountAuthenticated.html',{'object':args[0]})
        a_citizen_02.sendEmailEWrapper(args[1], subject, [args[0].direct.email], bodyText=bodyText)         
        
    elif args[0].authenticated == '-1':     
        a_citizen_02.sendUserMessage(args[1], "Denied authentication",          toCitizen=args[0], type='sys', body=args[2]['reasonfordeny'])


#### *********************************************************
###def BLOCK_LogIn(request):
###    loginContextDict = {}
###    formResultDict = FORM_Login(request)
###    if not formResultDict['redirect']:
###        loginContextDict['form_itself'] = formResultDict['display']
###        loginContextDict['form_errors'] = formResultDict['error']
###        return a_citizen_02.processTemplate_01(request, 'a_citizen_02/templates/BLOCK_LogIn.html', loginContextDict)
###    else:
###        return BLOCK_LoggedIn(request)
###    
#### *********************************************************
###def FORM_Login(request):
###    formClass = Form_engine_menu_a_Login
###    form_action = request.META['duo_FormActionPrepend'] + request.META['PATH_INFO']
###    resultDict = a_citizen_02.processForm_01(request, formClass, None, 'a_citizen_02/templates/FORM_Login.html', resetFormOnSuccess=True, form_action=form_action)
###    
###    if resultDict['success']:
###        # make sure the user exists
###        user = authenticate(username=resultDict['cleanData']['username'], password=resultDict['cleanData']['password'])        
###        if user is not None:
###            if user.is_active:
###                from a_library_02 import engine_permissions
###                from a_mgrApplication_03.models import a_mgrApplication_03
###                
###                # log them in
###                login(request, user)
###                request.META['duo_citizen'] = a_citizen_02.getCurrentFromDirect(request)
###                engine_permissions.setUserPermissions(request)
###                a_mgrApplication_03.mw_request_citizenDetails(request)
###                
###                return {'redirect':True, 'display':'dislay BLOCK_LoggedIn'}
###            else:
###                # generate error if that user account is no longer active
###                error_message = "Your account has been disabled!"
###                return {'redirect':False,'display':resultDict['out'],'error':error_message}
###        else:
###            # generate error if the user could not be logged in
###            error_message = "Your username or password was incorrect."
###            return {'redirect':False,'display':resultDict['out'],'error':error_message}
###    else: 
###        error_message = ""
###        return {'redirect':False,'display':resultDict['out'],'error':error_message}

#### *********************************************************
###def FORM_MenuViews(request, currentView):
###    formClass = Form_engine_viewMenu_a
###    form_action = request.META['duo_FormActionPrepend'] + request.META['PATH_INFO']
###    resultDict = a_citizen_02.processForm_01(
###                                              request, 
###                                              formClass, 
###                                              None, 
###                                              'a_citizen_02/templates/FORM_MenuViews.html', 
###                                              resetFormOnSuccess=True, 
###                                              form_action=form_action, 
###                                              toFormDict={'request':''}  
###                                              )
###    return resultDict

#### I dont think this is being used anywhere
##### *********************************************************
####def BLOCK_FlatNavigationMenu(request, navLinkList):
####    navLinkList.sort()
####    return a_citizen_02.processTemplate_01(request, 'a_citizen_02/templates/BLOCK_FlatNavigationMenu.html', {'objectList': navLinkList})

### *********************************************************
##def BLOCK_Citizen(request):
##    if request.META['duo_Direct']: return BLOCK_CitizenDirect(request)
##    else:                          return BLOCK_CitizenFacebook(request)

### *********************************************************
##def BLOCK_CitizenDirect(request):
##    if request.user.id is None: block = BLOCK_LogIn(request)
##    else:                       block = BLOCK_LoggedIn(request)
##    return block    

#### *********************************************************
###def BLOCK_LoggedIn(request):
###    msgUser_link        = reverse('a_msgUser_02_VIEW_List',         urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) 
###    msgSocial_link      = reverse('a_msgSocial_02_VIEW_List',       urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) 
###    msgReply_link       = reverse('e_thread_03_VIEW_List',          urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) 
###    prefs_link          = reverse('a_citizen_02_VIEW_Preferences',  urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) 
###    
###    return a_citizen_02.processTemplate_01(request, 'a_citizen_02/templates/BLOCK_loggedin.html', {'prefs_link':prefs_link,'msgUser_link':msgUser_link,'msgSocial_link':msgSocial_link,'msgReply_link':msgReply_link})

#### *********************************************************
###def BLOCK_CitizenFacebook(request):
###    
#####    # extract and process fb_sug post elements from POST for display
#####    for key, value in request.POST.items():
#####            if key == "fb_sig_user": 
#####            elif key == "fb_sig_added": 
#####            elif key == "fb_sig_session_key": 
#####            elif key == "fb_sig_expires": 
#####            elif key == "fb_sig": 
#####            elif key == "fb_sig_time": 
#####            elif key == "fb_sig_profile_update_time": 
#####            elif key == "fb_sig_api_key": 
#####            elif key == "fb_sig_friends": 
#####            elif key == "fb_sig_locale": 
#####            elif key == "fb_sig_position_fix": 
#####            elif key == "fb_sig_request_method": 
#####            elif key == "fb_sig_in_canvas":
###
####    citizen = 'FB guest'
####    if 'fb_sig_user' in request.POST:
####        citizen = '<fb:name uid="'+request.POST['fb_sig_user']+'" firstnameonly="true" useyou="false" linked="false"/>'
####    block = a_citizen_02.processTemplate_01(request, 'a_citizen_02/templates/BLOCK_CitizenFacebook.html', {'citizen': citizen})
###    
###    msgUser_link        = reverse('a_msgUser_02_VIEW_List',     urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) 
###    msgSocial_link      = reverse('a_msgSocial_02_VIEW_List',   urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) 
###    msgReply_link       = reverse('e_thread_03_VIEW_List',      urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) 
###    return a_citizen_02.processTemplate_01(request, 'a_citizen_02/templates/BLOCK_loggedin.html', {'msgUser_link':msgUser_link,'msgSocial_link':msgSocial_link,'msgReply_link':msgReply_link})

# *********************************************************
def a_urlPassChange_02_VIEW_List(request):
    QS = a_urlPassChange_02.objects.order_by('rand1')
    return a_urlPassChange_02.auto_list(request, QS)

# *********************************************************
def a_urlPassChange_02_VIEW_changeRequestSent(request):
    contextDict = {}
    contextDict['vTitle'] = "Password Change Request Sent"
    contextDict['main_1'] = "An email has been sent to your address. Click on the link enclosed to access the password change form."
    return a_urlPassChange_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')

# *********************************************************
def a_urlPassChange_02_VIEW_changeRequest(request):
        
    fn_dict = {'success' : RequestPassChange_processSuccess}
    rDict = a_urlPassChange_02.auto_form(
                                      request, 
                                      Form_a_urlPassChange_02_passChange, 
                                      fn_dict, 
                                      'a_urlPassChange_02_VIEW_changeRequest', 
                                      'F_passChange.html', 
                                      redirectOnSuccess=True,
                                      )
    if rDict['success']:
        return a_urlPassChange_02.redirectView(request, 'a_urlPassChange_02_VIEW_changeRequestSent', 'admFormPr')
    else:
        contextDict = {}
        contextDict['main_1']                       = rDict['out']
        return a_urlPassChange_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')

# *********************************************************
def RequestPassChange_processSuccess(*args):
    # args[0] = i (the instance)
    # args[1] = request
    # args[2] = cleanDataDict
    # args[3] = redirectReason  
    
    userInst = User.objects.get(username__exact=args[2]['username'], email__exact=args[2]['email']) 

    # Generate a_urlPassChange_02 instance and put equivalent url into the mail
    instance = a_urlPassChange_02()
    instance.user = userInst
    instance.save(request=args[1])
    
    subject                = "Password Change Request"
    bodyTemplate           = 'BLOCK_passChangeRequestEmail.html'
    bodyContextDict        = {'BASE_URL':settings.DIRECT_HTTP_HOST, 'validtionURL':instance.returnValidationUrl(args[1])}
    a_urlPassChange_02.sendEmailEWrapper(args[1], subject, [args[2]['email']], bodyTemplate=bodyTemplate, bodyContextDict=bodyContextDict)    

# *********************************************************
def a_urlPassChange_02_VIEW_validateEmail(request, userId, rand1, rand2):
    validationMessage  = ''    
    QS = a_urlPassChange_02.objects.filter(user__id__exact=userId, rand1__exact=rand1, rand2__exact=rand2)
    if QS.count():
        # save the a_urlPassChange_02 instance
        instance = QS[0]
        userInstance = User.objects.get(id__exact=userId)
        
        fn_dict = {'success' : PassChange_processSuccess}
        rDict = a_urlPassChange_02.auto_form(
                                          request, 
                                          Form_a_urlPassChange_02_editPassword, 
                                          fn_dict, 
                                          'a_urlPassChange_02_VIEW_validateEmail', 
                                          'FORM_ChangePassword.html', 
                                          workObj=userInstance,
                                          redirectOnSuccess=True,
                                          viewName_kwargs = {'userId':userId, 'rand1':rand1, 'rand2':rand2}
                                          )
        if rDict['success']:
            # delete the a_urlPassChange_02 instance
            instance.delete(request=request)            
            validationMessage = 'Password changed'
        else:
            contextDict = {}
            contextDict['main_1'] = rDict['out']
            return a_urlPassChange_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')    
        
    else:
        validationMessage = 'Invalid password change request URL'
       
    contextDict = {}
    contextDict['main_1'] = validationMessage    
        
    return a_urlPassChange_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')

# *********************************************************
def PassChange_processSuccess(*args):
    # args[0] = i (the instance)
    # args[1] = request
    # args[2] = cleanDataDict
    # args[3] = redirectReason   

    userInst = args[0]
    userInst.set_password(args[2]['new_pass1'])
    userInst.save()
    
# *********************************************************
def a_citizen_02_VIEW_Register(request, cit_id='', rv1='', rv2=''):
    
    
    contextDict         = {'vTitle':'New Citizen Registration'}    
    action_view         = 'a_citizen_02_VIEW_Register'
    action_kwargs       = {}

    # Later if this is non zero it contains the citizen_id of the user who issued this invite
    inviteRegistration = 0
    
    if cit_id and rv1 and rv2:
        # Determine if the request exists
        try:
            friend = a_citizen_02.objects.get(pk=cit_id)
            qs = a_friends_externalRequest_01.objects.get(citizen=friend, rand_value1=rv1, rand_value2=rv2)
            inviteRegistration  = cit_id
            action_kwargs       = {'cit_id':cit_id,'rv1':rv1,'rv2':rv2,}
        except ObjectDoesNotExist:
            pass
        
    form_action         = a_citizen_02.build_form_action(request, action_view, action_kwargs)
    
    form_class          = Form_a_citizen_02_registerNewUser
    form_object         = None                                                                       
    form_template       = 'F_register.html'
    form_context_dict   = {}
    form_build_dict     = {}                                                                                    
    result_dict         = a_citizen_02.get_result_dict(request, form_action, form_class, form_object, form_template, form_context_dict, form_build_dict, resetFormOnSuccess=True)    
    
    if result_dict['success']:
        from a_mgrApplication_03.views import a_mgrApplication_03_newCitizenDefaultSubscriptions
        instance = result_dict['formInstance'].save(commit=False) 

        # -----------------------------------------------------
        # process form results
        # conversion: args[0] = instance, args[1] = request, args[2] = result_dict['cleanData'], args[3] = redirectReason   
        
        # save user object
        user = User.objects.create_user(result_dict['cleanData']['userName'], result_dict['cleanData']['email'], result_dict['cleanData']['pass1'])
        user.first_name = result_dict['cleanData']['firstName']
        user.last_name  = result_dict['cleanData']['lastName']
        user.save()
        
        # create citizen object
        citizenInstance =  a_citizen_02.birthNewCitizen(request, direct=user, reasonJoined=result_dict['cleanData']['reasonJoined'])
    
        a_citizen_02.sendUserMessage(request, "Welcome to %s." % (settings.SITE_NAME), toCitizen=citizenInstance, body="Please validate your email address by clicking on the link in the email that was sent to %s."%(user.email), type='sys')
        
        # Manually log this user in
        user = authenticate(username=result_dict['cleanData']['userName'], password=result_dict['cleanData']['pass1'])        
        if user is not None and user.is_active:
            login(request, user)   
            
        # auto subscribe user to all apps
        request.META['duo_citizen'] = a_citizen_02.getCurrentFromDirect(request)            
        a_mgrApplication_03_newCitizenDefaultSubscriptions(request)
                
        # Generate email validation instance and put equivalent url into the mail
        a_mgrEmailValidate_02_instance = a_mgrEmailValidate_02()
        a_mgrEmailValidate_02_instance.user = user
        a_mgrEmailValidate_02_instance.save(request=request)
        
        invite_friendRequest = ''
        if inviteRegistration:
            a_friends_externalRequest_01.approve(request, friend, rv1, rv2, citizenInstance)
            invite_friendRequest = 'Your friendship with %s is ready pending approval from them.' % (friend)
        
        subject                = "Welcome to %s" % (settings.SITE_NAME)
        bodyTemplate           = 'E_welcome.html'
        bodyContextDict        = {
                                    'BASE_URL'              : settings.DIRECT_HTTP_HOST, 
                                    'validtionURL'          : a_mgrEmailValidate_02_instance.returnValidationUrl(request),
                                    'invite_friendRequest'  : invite_friendRequest,
                                    'site_name'             : settings.SITE_NAME,
                                 }
    
        a_citizen_02.sendEmailEWrapper(request, subject, [user.email], bodyTemplate=bodyTemplate, bodyContextDict=bodyContextDict)   
        # -----------------------------------------------------

        return a_citizen_02.redirectView(request, 'a_citizen_02_VIEW_Welcome', 'welcome')
    else:
        contextDict['main_1'] = result_dict['out']
        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')    


# *********************************************************
def a_citizen_02_VIEW_PreferencesEditPassword(request):
#    contextDict         = {'vTitle':'Edit Password'}    
    contextDict         = {}    
    citizen             = request.META['duo_citizen']
    
    action_view         = 'a_citizen_02_VIEW_PreferencesEditPassword'
    action_kwargs       = {}
    form_action         = a_citizen_02.build_form_action(request, action_view, action_kwargs)
    
    form_class          = Form_a_citizen_02_editPassword
    form_object         = citizen
    form_template       = 'F_editPassword.html'
    form_title          = 'Edit Password'
    form_context_dict   = {'form_title':form_title}
    form_build_dict     = {}
    result_dict         = a_citizen_02.get_result_dict(request, form_action, form_class, form_object, form_template, form_context_dict, form_build_dict, resetFormOnSuccess=True)    
    
    if result_dict['success']:
        instance = result_dict['formInstance'].save(commit=False) 

        # -----------------------------------------------------
        # process form results
        # conversion: args[0] = instance, args[1] = request, args[2] = result_dict['cleanData'], args[3] = redirectReason  
        userInst = instance.direct
        userInst.set_password(result_dict['cleanData']['new_pass1'])
        userInst.save()        
        # -----------------------------------------------------
    
        result_text = 'Password changed'
        contextDict = {'vTitle':'Success'}    
        contextDict['main_1'] = a_citizen_02.processTemplate_01(request,'a_citizen_02/templates/R_preferences.html',{'result_text':result_text})    
        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')  
    else:
        contextDict['main_1'] = result_dict['out']
        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')       

# *********************************************************
def a_citizen_02_VIEW_PreferencesEditEmail(request):
#    contextDict         = {'vTitle':'Edit Email Address'}    
    contextDict         = {}    
    citizen             = request.META['duo_citizen']
    
    action_view         = 'a_citizen_02_VIEW_PreferencesEditEmail'
    action_kwargs       = {}
    form_action         = a_citizen_02.build_form_action(request, action_view, action_kwargs)
    
    form_class          = Form_a_citizen_02_editEmail
    form_object         = citizen.direct
    form_template       = 'F_editEmail.html'
    form_title          = 'Edit Email Address'
    form_context_dict   = {'form_title':form_title}
    form_build_dict     = {}
    result_dict         = a_citizen_02.get_result_dict(request, form_action, form_class, form_object, form_template, form_context_dict, form_build_dict, resetFormOnSuccess=True)    
    
    if result_dict['success']:
        instance = result_dict['formInstance'].save(commit=False) 

        # -----------------------------------------------------
        # process form results
        # conversion: args[0] = instance, args[1] = request, args[2] = result_dict['cleanData'], args[3] = redirectReason  
        
        instance.email = result_dict['cleanData']['email']
        instance.save()        
        # -----------------------------------------------------
    
        result_text = 'Email address changed to %s' % (result_dict['cleanData']['email'])
        contextDict = {'vTitle':'Success'}    
        contextDict['main_1'] = a_citizen_02.processTemplate_01(request,'a_citizen_02/templates/R_preferences.html',{'result_text':result_text})    
        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')    
    else:
        contextDict['main_1'] = result_dict['out']
        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')       
    
# *********************************************************
def a_citizen_02_VIEW_AnotherEmailValidation(request):
    
    contextDict = {}    
    if not request.META['duo_citizen'].directEmailValidated: 
        citizen = request.META['duo_citizen']
          
        # Generate email validation instance and put equivalent url into the mail
        a_mgrEmailValidate_02_instance = a_mgrEmailValidate_02()
        a_mgrEmailValidate_02_instance.user = citizen.direct
        a_mgrEmailValidate_02_instance.save(request=request)
        
        subject                = "Welcome to %s" % (settings.SITE_NAME)
        bodyTemplate           = 'E_welcome.html'
        bodyContextDict        = {
                                    'BASE_URL'              : settings.DIRECT_HTTP_HOST, 
                                    'validtionURL'          : a_mgrEmailValidate_02_instance.returnValidationUrl(request),
                                    'invite_friendRequest'  : '',
                                    'site_name'             : settings.SITE_NAME,
                                 }
    
        a_citizen_02.sendEmailEWrapper(request, subject, [citizen.direct.email], bodyTemplate=bodyTemplate, bodyContextDict=bodyContextDict) 

        result_text = 'Email validation Email sent to %s' % (citizen.direct.email)
        contextDict = {'vTitle':'Success'}    
    else:
        result_text = 'Email validation Email NOT sent. Your email address is already validated'
        contextDict = {'vTitle':'Error'}    

    contextDict['main_1'] = a_citizen_02.processTemplate_01(request,'a_citizen_02/templates/R_preferences.html',{'result_text':result_text})    
    return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')          
    
# *********************************************************
def a_citizen_02_VIEW_AnotherAuthorization(request):
    contextDict         = {'vTitle':'Request Authorization Again'}    
    citizen             =  request.META['duo_citizen']
    
    action_view         = 'a_citizen_02_VIEW_AnotherAuthorization'
    action_kwargs       = {}
    form_action         = a_citizen_02.build_form_action(request, action_view, action_kwargs)
    
    form_class          = Form_a_citizen_02_requestAuthorizationAgain
    form_object         = citizen
    form_template       = 'F_requestAnotherAuthorization.html'
    form_title          = 'Request Authorization Again'
    form_context_dict   = {'form_title':form_title}
    form_build_dict     = {}
    result_dict         = a_citizen_02.get_result_dict(request, form_action, form_class, form_object, form_template, form_context_dict, form_build_dict, resetFormOnSuccess=True)    
    
    if result_dict['success']:
        instance = result_dict['formInstance'].save(commit=False) 

        # -----------------------------------------------------
        # process form results
        # conversion: args[0] = instance, args[1] = request, args[2] = result_dict['cleanData'], args[3] = redirectReason  

        instance.authenticated       = 0
        instance.authenticated_count -= 1
        instance.save()        
        # -----------------------------------------------------
    
        result_text = 'Another request for authorization has been submitted'
        contextDict = {'vTitle':'Success'}    
        contextDict['main_1'] = a_citizen_02.processTemplate_01(request,'a_citizen_02/templates/R_preferences.html',{'result_text':result_text})    
        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')    
    else:
        contextDict['main_1'] = result_dict['out']
        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')       

# *********************************************************
def prefEntry_email(request):
    prefEntry = {}
    prefEntry['title']        = 'Email Address'
    prefEntry['editLink']     = "<a href='%s'>%s</a>" % (reverse('a_citizen_02_VIEW_PreferencesEditEmail', kwargs = {}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , 'edit')
    return prefEntry

# *********************************************************
def prefEntry_password(request):
    prefEntry = {}
    prefEntry['title']        = 'Password'
    prefEntry['editLink']     = "<a href='%s'>%s</a>" % (reverse('a_citizen_02_VIEW_PreferencesEditPassword', kwargs = {}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , 'edit')
    return prefEntry

# *********************************************************
def prefEntry_rerequestEmailValidation(request):
    prefEntry = {}
    prefEntry['title']        = 'Request Another Email Validation Email'
    prefEntry['editLink']     = "<a href='%s'>%s</a>" % (reverse('a_citizen_02_VIEW_AnotherEmailValidation', kwargs = {}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , 'yes')
    return prefEntry

# *********************************************************
def prefEntry_rerequestAuthorization(request):
    prefEntry = {}
    prefEntry['title']        = 'Request Authorization Again'
    prefEntry['editLink']     = "<a href='%s'>%s</a>" % (reverse('a_citizen_02_VIEW_AnotherAuthorization', kwargs = {}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , 'yes')
    return prefEntry

# *********************************************************
def a_citizen_02_VIEW_Preferences(request):
    contextDict = {}
    prefList    = []
#    citizen     = request.META['duo_citizen']
    
    if request.META['citizen_rights'] == secDict['s_denied']:
        if request.META['duo_Direct']: prefList.append(prefEntry_rerequestAuthorization(request))
    else:
        if request.META['duo_Direct']: prefList.append(prefEntry_email(request))
        if request.META['duo_Direct']: prefList.append(prefEntry_password(request))
        if not request.META['duo_citizen'].directEmailValidated: prefList.append(prefEntry_rerequestEmailValidation(request))
    
    contextDict['vTitle'] = "Citizen Settings" 
    contextDict['main_1'] = a_citizen_02.processTemplate_01(request, 'B_preferences.html',{'prefList':prefList})   
    return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')    