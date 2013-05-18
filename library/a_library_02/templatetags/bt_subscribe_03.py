# *********************************************************
# bt_subscribe_03.py

## *********************************************************
from django import template
from django.conf import settings
from django.template import resolve_variable
from django.contrib.contenttypes.models import ContentType
from a_mgrApplication_03.models import genericUserAppSubscription
from django.core.urlresolvers import reverse

register = template.Library()

# *********************************************************
class bt_subscribe_03(template.Node):   
    
    
    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        self.paramDict      = paramDict
        self.errorList      = errorList
        self.resolveDict    = resolveDict
        self.requiredParam  = ["OBJECT", "MODE"]
        
        
    # *********************************************************
    def render(self, context):
        returnList = []
        
        # Get the request variable from the context
        request = resolve_variable('request', context)  
        
        if settings.DEBUG:
            for param in self.requiredParam:
                if param not in self.paramDict:
                    self.errorList.append("Did not find self.requiredParam : %s" % (param))
               
        for key, value in self.resolveDict.items():
             self.paramDict[key] = value.resolve(context)

        # -----------------------------------------------------
        urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)        
        ajaxProcessingUrl = reverse('a_mgrApplication_03_VIEW_genericUserAppSubscriptionToggle', kwargs = {}, urlconf=urlconf)   
        
        if request.META['duo_citizen']:
            QS = genericUserAppSubscription.objects.filter(
                                                           auto_object_id__exact        = self.paramDict['OBJECT'].id,
                                                           auto_content_type__exact     = ContentType.objects.get_for_model(self.paramDict['OBJECT']),
                                                           auto_citizen__exact          = request.META['duo_citizen']
                                                           )
            
            linkTextList = []
            linkTextList.append('<a')
            linkTextList.append(' href="#"')
            
            linkTextList.append(' onclick="return toggle_subscription_03(this,')
            linkTextList.append("%s"%(self.paramDict['OBJECT'].id))
            linkTextList.append(',')
            linkTextList.append("'%s'"%(ContentType.objects.get_for_model(self.paramDict['OBJECT'])))
            linkTextList.append(',')
            linkTextList.append("'%s'"%(ajaxProcessingUrl))
            linkTextList.append(')">')
                    
            if QS.count():      linkTextList.append('Un-Subscribe')
            else:               linkTextList.append('Subscribe')
            
            linkTextList.append('</a>')
            
            fullLink = ''.join(linkTextList)
#            print "*** fullLink = %s" % (fullLink)
            returnList.append(fullLink)
        # -----------------------------------------------------
        
        if settings.DEBUG:
            for x in self.errorList:
                returnList.append("<br/>%s"%(x))

        return ''.join(returnList)
