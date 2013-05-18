# *********************************************************
# a_msgSocial_02/models.py

# *********************************************************
from a_base_02.models import a_base_02
from a_citizen_02.models import a_citizen_02
from django import forms
from django.db import models
from django.forms import ModelForm
import cPickle
import settings

allMessageDict = {}
allMessageRelationToClassDict = {}
       
# *********************************************************
class a_msgSocial_02(a_base_02):
    messageName            = models.CharField        (max_length = '24')
    destination            = models.CharField        (max_length = '12')
    priority               = models.CharField        (max_length = '8')
    _kwargs                = models.TextField        (blank = True)
    status                 = models.CharField        (max_length = '8', default="pending")
    sentTitle              = models.CharField        (blank=True, null=True, max_length = '300')
    sentBody               = models.CharField        (blank=True, null=True, max_length = '300')
    sentBodyGeneral        = models.CharField        (blank=True, null=True, max_length = '300')
    auto_fields            = ['auto_versioned']
    
####    # -----------------------------------------------------
####    # THIS HASN'T REALLY BEEN TESTED AS I MADE THE CHANGE WHEN IMPLEMENTING THIS BUT
####    # DIDN'T HAVE SOCIAL MESSAGES WORKING TO TEST. THIS WAS COPIED FROM msgUser's implementation.
####    # For instance the query used below is wrong as a_msgSocial_02 doesn't have a toCitizen field any more
####    def msgSocialRender(request):
####        displayText = 'social messages'
####        if request.META['auto_currentView'] == 'a_msgSocial_02_VIEW_List':
####            returnString = "<a href='%s' id='citizenNav-on'>%s</a>" % (reverse('a_msgSocial_02_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
####        else:
####            if a_msgSocial_02.objects.filter(toCitizen__exact=request.META['duo_citizen'], read__exact=False).count():
####                returnString = "<a href='%s' id='citizenNav-attention'>%s</a>" % (reverse('a_msgSocial_02_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
####            else:
####                returnString = "<a href='%s'>%s</a>" % (reverse('a_msgSocial_02_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
####        return returnString
####    msgSocialRender = staticmethod(msgSocialRender)    
    
    # -----------------------------------------------------
    def viewSecurityLookupMethod(viewName):
        from a_base_02.models import secDict
        local_ViewDict = {}
        local_ViewDict['a_msgSocial_02_VIEW_List']    = secDict['s_citizen']
        
        if viewName not in local_ViewDict: return secDict['s_undefined']
        else:                              return local_ViewDict[viewName]  
    viewSecurityLookupMethod = staticmethod(viewSecurityLookupMethod)

    # -----------------------------------------------------
    def __unicode__(self):          return u'%s: destination(%s), kwargs(%s)' % (self.messageName, self.destination, self.kwargs)
    def get_absolute_url(self):     return "/a_msgSocial_02/%i/" % self.id
    def delete(self, **kwargs):     super(a_msgSocial_02, self).delete(**kwargs)
    def save(self, **kwargs):       super(a_msgSocial_02, self).save(**kwargs)   
    
    # -----------------------------------------------------
    def _get_kwargs(self):
        returnDict = {}
        if (self._kwargs): returnDict = cPickle.loads(self._kwargs.encode('ascii'))
        return returnDict
    def _set_kwargs(self, xDict):
        self._kwargs =  cPickle.dumps(xDict)
    kwargs = property(_get_kwargs, _set_kwargs)    

    # -----------------------------------------------------
    def processMessageDictEntry(key, value, className):
        # make sure this message has all required attributes defined
        requiredValueAttributeError = False
        requiredValueAttribute = ['destination', 'priority', 'template', 'kwargs']
        for x in requiredValueAttribute:
            if not value.has_key(x):
                requiredValueAttribsError = True
                print "ERROR: (%s): requiredValueAttribute (%s) not defined." % (key, x)
                
        validKwargTypes = ['value', 'instance', 'fb_uid']
        for k, v in value['kwargs'].items(): 
            if v[0] not in validKwargTypes:    
                print "ERROR: (%s) unrecognized kwarg type (%s)" % (key, v[0]) 
                
        if not requiredValueAttributeError:
            allMessageDict[key] = value
            allMessageRelationToClassDict[key] = className
    processMessageDictEntry = staticmethod(processMessageDictEntry)

    # -----------------------------------------------------
    # title_template parameter is required, and is limited to 60 displayed characters (excluding tags) 
    # The body_template is optional, and is limited to 200 display characters when combined with body_general (excluding tags)   
    def renderMessage(self, request):
        kwargsProcessed = renderKwargs(request, self.messageName, self.kwargs)
        self.sentTitle       = a_msgSocial_02.processTemplate_01(request, allMessageDict[self.messageName]['template'], {'kwargs': kwargsProcessed,'message_mode':'title'}).strip()
        self.sentBody        = a_msgSocial_02.processTemplate_01(request, allMessageDict[self.messageName]['template'], {'kwargs': kwargsProcessed,'message_mode':'body'}).strip()
        self.sentBodyGeneral = a_msgSocial_02.processTemplate_01(request, allMessageDict[self.messageName]['template'], {'kwargs': kwargsProcessed,'message_mode':'bodygeneral'}).strip()
        
# -----------------------------------------------------
def renderKwargs(request, messageName, paramKwargs):
    returnDict = {}

    for k, v in paramKwargs.items():
        if allMessageDict[messageName]['kwargs'][k][0] == "instance":
            from a_base_02.models import allClassesDict
            returnDict[k] = allClassesDict[allMessageRelationToClassDict[messageName]].objects.get(id=v)
        else:
            returnDict[k] = v
        
    return returnDict
        
# -----------------------------------------------------
def processKwargs(request, messageName, paramKwargs):
    returnDict = {}
    for k, v in allMessageDict[messageName]['kwargs'].items():
        VAL = ''
        if len(v)==3 or paramKwargs.has_key(k):
            if paramKwargs.has_key(k): 
                VAL = paramKwargs[k]
                del paramKwargs[k]
            else:                               
                VAL = v[2]     
                   
        if VAL:
            if v[0] == "instance": 
                VAL = VAL.id        
            returnDict[k] = VAL
        elif v[1] == 'required': print "ERROR: (%s) - required kwarg (%s) doesn't have a default or a paramKwargs value." % (messageName, k)        
    if len(paramKwargs): print "ERROR: paramKwargs (%s) seems to have extra values which were not processed" % (paramKwargs)
    return returnDict
        
# -----------------------------------------------------
def internalQueueSocialMessage(messageName, kwargs, request, destination='', priority='',):
    returnValue = None
    
    if allMessageDict.has_key(messageName):
        finalDestination = allMessageDict[messageName]['destination']
        finalPriority    = allMessageDict[messageName]['priority']
        if destination:    finalDestination = destination
        if priority:       finalPriority    = priority
        
        # EVENTUALLY NEED SOMETHING LIKE ...
        # if destinationCitizen = 'all_application_users' then dispatch message to all application users

        # if expecting some kwargs then some better have been passed in and of course the (i.e. expecting no kwargs)
        if not (allMessageDict[messageName]['kwargs'] and not kwargs) or (not allMessageDict[messageName]['kwargs'] and kwargs):
            if allMessageDict[messageName]['kwargs']: # parse and compare kwargs given versus expected
                finalKwargs = processKwargs(request, messageName, kwargs)
                messageInst = a_msgSocial_02(messageName=messageName, destination=finalDestination, priority=finalPriority, kwargs=finalKwargs, auto_citizen=request.META['duo_citizen'])
                messageInst.save(request=request)
                returnValue = messageInst
        else:
            print "ERROR: kwargs irregularity, expecting (%s) but recieved (%s)" % (allMessageDict[messageName]['kwargs'], kwargs) 
    else:
        print "ERROR: unknown message (%s)" % (messageName) 
        
    return returnValue
