# *********************************************************
# a_mgrEmail_02/models.py

# *********************************************************
from a_base_02.models import a_base_02
from a_library_02 import engine_signals
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models, models
from django.dispatch import dispatcher, Signal
from django.forms import ModelForm
import cPickle
import random
import settings
import threading
import time

# *********************************************************
emailSignalX = Signal()  

# *********************************************************
class thread_sendEmail(threading.Thread):  
    def __init__(self, subject, body, to, request, a_mgrEmail_02_instance):  
        self.subject                        = subject
        self.body                           = body
        self.to                             = to
        self.request                        = request
        self.a_mgrEmail_02_instance = a_mgrEmail_02_instance
        self.contents                       = a_mgrEmail_02.processTemplate_01(request, 'EMAIL_base.html', {'bodyList':self.body})
        threading.Thread.__init__(self)
        print "+++ thread_sendEmail: started"
           
    def run (self):  
        from django.core.mail import EmailMessage  
        eMsg = EmailMessage(subject=self.subject, body=self.contents, to=self.to)
        eMsg.send()
        self.a_mgrEmail_02_instance.sent = True
        self.a_mgrEmail_02_instance.save(request=self.request)
        print "+++ thread_sendEmail: completed"
        
# *********************************************************
def process_emailSignalX(sender, subject, body, to, signal, request, a_mgrEmail_02_instance, *args, **kwargs):  
    thread_sendEmail(subject, body, to, request, a_mgrEmail_02_instance).start()

# *********************************************************
class a_mgrEmail_02(a_base_02):
    subject           = models.CharField        (max_length = 150)
    _toList           = models.TextField        ()     
    bodyTemplate      = models.CharField        (max_length = 150, blank = True, null = True)
    _bodyContextDict  = models.TextField        (blank = True, null = True)   
    bodyText          = models.TextField        (blank = True, null = True)     
    sent              = models.BooleanField     (default=False)
    auto_fields       = ['auto_citizenNull', 'auto_timeStamp'] 
    
    # -----------------------------------------------------
    def entryInit_c_nav_02_menu(cls):
        menuDict = []  
###        menuDict.append({
###                            'displayText'                           :   'email manager',
###                            'menu'                                  :   'SIDE',
###                            'view'                                  :   'a_mgrEmail_02_VIEW_List',
###                            'priority'                              :   3,
###                            'isLocal'                               :   False,
###                            'parentViewList'                        :   [],
###                            'required_viewParamsList'               :   [],
###                            'altSelectOnViewList'                   :   [],
###                            'renderMethod'                          :   '',
###                            'criteriaMethod'                        :   '',
###                       })  
        return menuDict 
    entryInit_c_nav_02_menu = classmethod(entryInit_c_nav_02_menu)       
    
    # -----------------------------------------------------
    def viewSecurityLookupMethod(viewName):
        from a_base_02.models import secDict
        local_ViewDict = {}
        local_ViewDict['a_mgrEmail_02_VIEW_List']               = secDict['s_developer']
        local_ViewDict['a_mgrEmail_02_VIEW_ValidateEmail']      = secDict['s_guest']
        
        if viewName not in local_ViewDict: return secDict['s_undefined']
        else:                                      return local_ViewDict[viewName]  
    viewSecurityLookupMethod = staticmethod(viewSecurityLookupMethod)     

    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.name)
    def get_absolute_url(self):     return "/a_mgrEmail_02/%i/" % self.id
    def delete(self, **kwargs):     super(a_mgrEmail_02, self).delete(**kwargs)
    def save(self, **kwargs):       super(a_mgrEmail_02, self).save(**kwargs)   
    
    # -----------------------------------------------------
    def _get_toList(self):
        returnList = []
        if (self._toList): returnList = cPickle.loads(self._toList.encode('ascii'))
        return returnList
    def _set_toList(self, xList):
        if xList:
            self._toList =  cPickle.dumps(xList)
    toList = property(_get_toList, _set_toList)    
        
    # -----------------------------------------------------
    def _get_bodyContextDict(self):
        returnDict = {}
        if (self._bodyContextDict): returnDict = cPickle.loads(self._bodyContextDict.encode('ascii'))
        return returnDict
    def _set_bodyContextDict(self, xDict):
        if xDict:
            self._bodyContextDict =  cPickle.dumps(xDict)
    bodyContextDict = property(_get_bodyContextDict, _set_bodyContextDict)    

    # -----------------------------------------------------
    def queueAndSend(request, subject, toList, bodyTemplate='', bodyContextDict={}, bodyText=''):
        contentsList = []
        
        if (bodyTemplate and bodyContextDict) or bodyText:
            if (bodyTemplate and bodyContextDict):
                contentsList.append(a_mgrEmail_02.processTemplate_01(request, bodyTemplate, bodyContextDict))
            if bodyText:
                contentsList.append(bodyText)
        else: 
            raise Exception, "queueAndSend(): requires either bodyTemplate + bodyContextDict or bodyText"  
        
        instance = a_mgrEmail_02()
        instance.subject           = subject
        instance.toList            = toList    
        instance.bodyTemplate      = bodyTemplate
        instance.bodyContextDict   = bodyContextDict   
        instance.bodyText          = bodyText
        instance.save(request=request)
            
        # send email message
        emailSignalX.connect(
                           process_emailSignalX, 
                           ) 
        emailSignalX.send(
                        subject = subject, 
                        body    = contentsList, 
                        to      = toList,
                        request = request,
                        sender  = a_mgrEmail_02.queueAndSend,
                        a_mgrEmail_02_instance = instance,
                        )              
    queueAndSend = staticmethod(queueAndSend)   
    
# *********************************************************
class a_mgrEmailValidate_02(a_base_02):
    rand1                = models.IntegerField       (max_length=14, blank=True, null=True)
    rand2                = models.IntegerField       (max_length=14, blank=True, null=True)
    user                 = models.ForeignKey         (User)
    
    auto_fields         = ['auto_timeStamp'] 
    
    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.user)
    def get_absolute_url(self):     return "/a_mgrEmailValidate_02/%i/" % self.id
    def delete(self, **kwargs):     super(a_mgrEmailValidate_02, self).delete(**kwargs)
    
    # -----------------------------------------------------
    # non standard save
    def save(self, **kwargs):  
        # Delete any existing instances for this user because "there can be only one"!
        QS = a_mgrEmailValidate_02.objects.filter(user__exact=self.user)
        for x in QS: 
#            x.delete(request=request)            
            x.delete()            
        
        timeNow = time.time()
        random.seed(timeNow)
        self.rand1 = int(random.random() * 100000000)
        self.rand2 = int(random.random() * 100000000) 
        super(a_mgrEmailValidate_02, self).save(**kwargs)   
        
    # -----------------------------------------------------
    def returnValidationUrl(self, request):
        return reverse('a_mgrEmail_02_VIEW_ValidateEmail', kwargs = {'userId':self.user.id,'rand1':self.rand1,'rand2':self.rand2}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))    
