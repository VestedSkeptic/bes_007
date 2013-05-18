# *********************************************************
# a_mgrEmail_02/views.py

# *********************************************************
from a_mgrEmail_02.models import a_mgrEmail_02, a_mgrEmailValidate_02
from django.contrib.auth.models import Permission
#from a_base_02.models import a_base_02
from a_citizen_02.models import a_citizen_02
import settings

# *********************************************************
def a_mgrEmail_02_VIEW_List(request):
    QS = a_mgrEmail_02.objects.order_by('id')
    return a_mgrEmail_02.auto_list(request, QS)

# *********************************************************
def a_mgrEmail_02_VIEW_ValidateEmail(request, userId, rand1, rand2):
    validationMessage  = ''    
    QS = a_mgrEmailValidate_02.objects.filter(user__id__exact=userId, rand1__exact=rand1, rand2__exact=rand2)
    if QS.count():
        # save the a_mgrEmailValidate_02 instance
        instance = QS[0]
        
        # set a_citizen_02_Instance.directEmailValidated to True
        QS = a_citizen_02.objects.filter(direct__exact=userId)
        a_citizen_02_Instance = QS[0]
        a_citizen_02_Instance.directEmailValidated = True
        a_citizen_02_Instance.save(request=request)
        
        # Display email is validated message
        validationMessage = 'Your email address was validated.'
        followMessage     = "Your account must still be authorized by the administrator before full participation is granted. This shouldn't take long."
        a_mgrEmailValidate_02.sendUserMessage(request, validationMessage, type='sys', toCitizen=a_citizen_02_Instance)          

        subject  = "user authorization required: [%s]" % a_citizen_02_Instance.name
        bodyText = ' '.join([subject,'id =',a_citizen_02_Instance.id.__str__()])
        a_mgrEmailValidate_02.sendEmailEWrapper(request, subject, [settings.SITE_ADMIN_EMAIL], bodyText=bodyText)      
        
        # delete the a_mgrEmailValidate_02 instance
        instance.delete(request=request)            
    else:
        validationMessage = 'Your email address was NOT validated.'
        followMessage     = 'Please make sure you clicked on the link in the email you recieved when you registered your account.'
       
    contextDict = {}
#    contextDict['vTitle'] = validationMessage    
#    contextDict['main_1'] = followMessage    
    contextDict['main_1'] = validationMessage    
    contextDict['main_2'] = followMessage    
        
    return a_mgrEmailValidate_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')