## old auto_form method of doing things

## *********************************************************
#def a_citizen_02_VIEW_Register(request):
#    contextDict = {}    
#    fn_dict = {'success' : Register_processSuccess}
#    rDict   = a_citizen_02.auto_form(
#                                      request, 
#                                      Form_a_citizen_02_registerNewUser, 
#                                      fn_dict, 
#                                      'a_citizen_02_VIEW_Register', 
##                                      'FORM_Register.html', 
#                                      'F_register.html', 
#                                      workObj=None,
#                                      redirectOnSuccess=True,
#                                    )
#
#    if rDict['success']:
#        return a_citizen_02.redirectView(request, 'a_citizen_02_VIEW_Welcome', 'welcome')
#    else:
#        contextDict['vTitle']                       = 'New User Registration'
#        contextDict['main_1']                       = rDict['out']
#        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')

## *********************************************************
#def Register_processSuccess(*args):
#    # args[0] = i (the instance)
#    # args[1] = request
#    # args[2] = cleanDataDict
#    # args[3] = redirectReason ('edit' or 'add')    
#
#    # save user object
#    user = User.objects.create_user(args[2]['userName'], args[2]['email'], args[2]['pass1'])
#    user.first_name = args[2]['firstName']
#    user.last_name  = args[2]['lastName']
#    user.save()
#    
#    # create citizen object
#    citizenInstance =  a_citizen_02.birthNewCitizen(args[1], direct=user, reasonJoined=args[2]['reasonJoined'])
#
#    a_citizen_02.sendUserMessage(args[1], "Welcome to the website.", toCitizen=citizenInstance, body="Don't forget to validate your email address by clicking on the link in the email that was sent to %s."%(user.email), type='sys')
#    
#    # Manually log this user in
#    user = authenticate(username=args[2]['userName'], password=args[2]['pass1'])        
#    if user is not None and user.is_active:
#        login(args[1], user)   
#            
#    # Generate email validation instance and put equivalent url into the mail
#    a_mgrEmailValidate_02_instance = a_mgrEmailValidate_02()
#    a_mgrEmailValidate_02_instance.user = user
#    a_mgrEmailValidate_02_instance.save(request=args[1])
#    
#    subject                = "welcome %s" % user.first_name
#    bodyTemplate           = 'E_welcome.html'
#
#    bodyContextDict        = {'BASE_URL':settings.DIRECT_HTTP_HOST, 'validtionURL':a_mgrEmailValidate_02_instance.returnValidationUrl(args[1])}
#
#    a_citizen_02.sendEmailEWrapper(args[1], subject, [user.email], bodyTemplate=bodyTemplate, bodyContextDict=bodyContextDict)


## *********************************************************
#def a_citizen_02_VIEW_PreferencesEditEmail(request, object_id):
#    contextDict = {}    
#    try:
#        citizen = a_citizen_02.objects.get(pk=object_id)
#    except a_citizen_02.DoesNotExist:
#        raise Http404    
#        
#    fn_dict = {'success' : editEmail_processSuccess}
#    rDict = a_citizen_02.auto_form(
#                                      request, 
#                                      Form_a_citizen_02_editEmail, 
#                                      fn_dict, 
#                                      'a_citizen_02_VIEW_PreferencesEditEmail', 
#                                      'F_editEmail.html', 
#                                      viewName_kwargs = {'object_id':object_id},
#                                      workObj=citizen.direct,
#                                      redirectOnSuccess=True,
#                                      )
#    if rDict['success']:
#        return a_citizen_02.redirectView(request, 'a_citizen_02_VIEW_Preferences', 'admFormPr')
#    else:
#        contextDict['main_1'] = rDict['out']
#        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')
#
## *********************************************************
#def editEmail_processSuccess(*args):
#    # args[0] = i (the instance)
#    # args[1] = request
#    # args[2] = cleanDataDict
#    # args[3] = redirectReason   
#    userInst = args[0]
#    userInst.email = args[2]['email']
#    userInst.save() 





    
#
## *********************************************************
#def a_citizen_02_VIEW_PreferencesEditPassword(request, object_id):
#    contextDict = {}    
#    try:
#        citizen = a_citizen_02.objects.get(pk=object_id)
#    except a_citizen_02.DoesNotExist:
#        raise Http404    
#        
#    fn_dict = {'success' : editPassword_processSuccess}
#    rDict = a_citizen_02.auto_form(
#                                      request, 
#                                      Form_a_citizen_02_editPassword, 
#                                      fn_dict, 
#                                      'a_citizen_02_VIEW_PreferencesEditPassword', 
#                                      'F_editPassword.html', 
#                                      viewName_kwargs = {'object_id':object_id},
#                                      workObj=citizen,
#                                      redirectOnSuccess=True,
#                                      )
#    if rDict['success']:
#        return a_citizen_02.redirectView(request, 'a_citizen_02_VIEW_Preferences', 'admFormPr')
#    else:
#        contextDict['main_1'] = rDict['out']
#        return a_citizen_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')
#
## *********************************************************
#def editPassword_processSuccess(*args):
#    # args[0] = i (the instance)
#    # args[1] = request
#    # args[2] = cleanDataDict
#    # args[3] = redirectReason   
#    userInst = args[0].direct
#    userInst.set_password(args[2]['new_pass1'])
#    userInst.save()