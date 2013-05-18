# *********************************************************
# bt_vote_03.py

## *********************************************************
from django import template
from django.conf import settings
from django.template import resolve_variable
from django.contrib.contenttypes.models import ContentType
from a_mgrApplication_03.models import genericUserAppVote, a_mgrApplication_03, genericUserAppVoteTotal
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

# *********************************************************
class bt_vote_03(template.Node):   
    
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
        
#        if request.META['duo_citizen']:
        try:
            totalInstance = genericUserAppVoteTotal.objects.get(
                                                           auto_object_id__exact        = self.paramDict['OBJECT'].id,
                                                           auto_content_type__exact     = ContentType.objects.get_for_model(self.paramDict['OBJECT']),
                                                           mode__exact                  = self.paramDict['MODE'],
                                                            )      
            currentTotal = totalInstance.total
        except ObjectDoesNotExist:
            currentTotal = 0
        
        try:
            usersCurrentVote = genericUserAppVote.objects.get(
                                                           auto_object_id__exact        = self.paramDict['OBJECT'].id,
                                                           auto_content_type__exact     = ContentType.objects.get_for_model(self.paramDict['OBJECT']),
                                                           mode__exact                  = self.paramDict['MODE'],
                                                           auto_citizen__exact          = request.META['duo_citizen'],
                                                           )
        except ObjectDoesNotExist:
            usersCurrentVote = ''

        currentVote = ''
        if usersCurrentVote:
            if   usersCurrentVote.vote == 1:  
                currentVote = 'up'
                possibleTotals = [currentTotal, currentTotal - 1, currentTotal - 2]
            elif usersCurrentVote.vote == -1: 
                currentVote = 'down'
                possibleTotals = [currentTotal + 2, currentTotal + 1, currentTotal]
        else:
            possibleTotals = [currentTotal + 1, currentTotal, currentTotal - 1]
            
        
        returnList.append(a_mgrApplication_03.processTemplate_01(
                                                                 request, 
                                                                 'BT_vote.html', 
                                                                 contextDict={
                                                                              'object_id'               : self.paramDict['OBJECT'].id,
                                                                              'content_type'            : ContentType.objects.get_for_model(self.paramDict['OBJECT']),
                                                                              'ajaxProcessingUrlUp'     : reverse('a_mgrApplication_03_VIEW_genericUserAppVote', kwargs = {'mode':self.paramDict['MODE'], 'vote': 1}, urlconf=urlconf),
                                                                              'ajaxProcessingUrlDown'   : reverse('a_mgrApplication_03_VIEW_genericUserAppVote', kwargs = {'mode':self.paramDict['MODE'], 'vote':-1}, urlconf=urlconf),
                                                                              'currentVote'             : currentVote,
                                                                              'currentTotal'            : currentTotal,
                                                                              'vote_1'                  : possibleTotals[0],
                                                                              'vote_2'                  : possibleTotals[1],
                                                                              'vote_3'                  : possibleTotals[2],
                                                                              }
                                                                     ))            
        # -----------------------------------------------------
        
        if settings.DEBUG:
            for x in self.errorList:
                returnList.append("<br/>%s"%(x))

        return ''.join(returnList)
