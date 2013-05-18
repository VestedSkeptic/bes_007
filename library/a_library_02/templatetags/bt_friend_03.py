# *********************************************************
# bt_friend_03.py

## *********************************************************
from a_base_02.models import a_base_02
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import resolve_variable
from django.core.exceptions import ObjectDoesNotExist
from a_friends_01.models import a_friends_internalRequest_01

register = template.Library()

# *********************************************************
class bt_friendBase_03(template.Node):   
    
    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        self.paramDict          = paramDict
        self.errorList          = errorList
        self.resolveDict        = resolveDict
        self.returnList         = []
        
    # *********************************************************
    def preRender_processing(self, context):
        if settings.DEBUG:
            for param in self.requiredParam:
                if param not in self.paramDict:
                    self.errorList.append("Did not find self.requiredParam : %s" % (param))
               
        for key, value in self.resolveDict.items():
             self.paramDict[key] = value.resolve(context)  
             
    # *********************************************************
    def postRender_processing(self):
        if settings.DEBUG:
            for x in self.errorList:
                self.returnList.append("<br/>%s"%(x))
        
# *********************************************************
class bt_friendRequestLink_03(bt_friendBase_03):   
    
    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        super(bt_friendRequestLink_03, self).__init__(paramDict, errorList, resolveDict)
        self.requiredParam  = ["OBJECT"]
        
    # *********************************************************
    def render(self, context):
        self.returnList     = []
        request = resolve_variable('request', context)              # Get the request variable from the context
        self.preRender_processing(context)
        
        # -----------------------------------------------------
        # Cant request friends with yourself                       and                 not an existing friend 
        if self.paramDict["OBJECT"] <> request.META['duo_citizen'] and self.paramDict["OBJECT"].id not in request.META['friendsIDlist']:
            try: # Determine if the request already exists
                qs = a_friends_internalRequest_01.objects.get(citizen=request.META['duo_citizen'], friend__id=self.paramDict["OBJECT"].id)
                self.returnList.append('friend request pending')
            except ObjectDoesNotExist:
                self.returnList.append("<a href='%s'>%s</a>" % (reverse('a_friends_01_VIEW_internalRequestAdd', kwargs = {'object_id':self.paramDict["OBJECT"].id}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), 'request friendship'))
        else:
            self.returnList.append(' ')     # For now I'm making sure something returns so there are no empty last div problems
        # -----------------------------------------------------
                        
        self.postRender_processing()
        return ''.join(self.returnList)
