# *********************************************************
# bt_interface_03.py

## *********************************************************
from a_base_02.models import a_base_02
from django import template
from django.conf import settings
from django.template import resolve_variable
from a_base_02.models import secDict
from django.core.urlresolvers import reverse
import settings

register = template.Library()

modesAvailableList = ['owner','s_citizen','s_admin','s_developer']

# *********************************************************
class bt_interface_03_delete(template.Node):
    
    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        self.paramDict      = paramDict
        self.errorList      = errorList
        self.resolveDict    = resolveDict
        self.requiredParam  = ["OBJECT","MODE","DELETECONFIRM"]
        
    # *********************************************************
    def render(self, context):
        return renderEditDelete(self, context, "Delete")

# *********************************************************
class bt_interface_03_edit(template.Node):   

    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        self.paramDict      = paramDict
        self.errorList      = errorList
        self.resolveDict    = resolveDict
        self.requiredParam  = ["OBJECT"]
        
    # *********************************************************
    def render(self, context):
        return renderEditDelete(self, context, "Edit")

# *********************************************************
def renderEditDelete(self, context, name):
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
    if settings.DEBUG and self.paramDict["MODE"] not in modesAvailableList:
        outText = "Unknown mode (%s). Available modes are: %s" % (self.paramDict['MODE'], ', '.join(modesAvailableList))
        self.errorList.append(outText)
        
    renderLink = False
    
    if request.META['duo_citizen'] is not None: 
        if self.paramDict["MODE"] == "owner":
            if request.META['duo_citizen'] == self.paramDict['OBJECT'].auto_citizen:
                renderLink = True
        elif self.paramDict["MODE"] == "s_admin" or self.paramDict["MODE"] == "s_developer" or self.paramDict["MODE"] == "s_citizen":
            if request.META['citizen_rights']['value'] >= secDict[self.paramDict["MODE"]]['value']:
                renderLink = True
    
    if renderLink:
        if not self.paramDict["DELETECONFIRM"]:
            
            # see if this is one of the newer classes that has the getUrl methods
            if hasattr(self.paramDict['OBJECT'], 'getUrl_edit'): 
                if name.lower() == "edit":  returnList.append(self.paramDict['OBJECT'].getUrl_edit(request, name))
                else :                      returnList.append(self.paramDict['OBJECT'].getUrl_delete(request, name))
            else:                                                  
                returnList.append("<a href='%s'>%s</a>" % (reverse("%s_VIEW_%s"%(self.paramDict['OBJECT'].__class__.__name__,name), kwargs = {'object_id':self.paramDict['OBJECT'].id},             urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , name.lower()))
        else:
            returnList.append("")
    # -----------------------------------------------------         
         
    if settings.DEBUG:
        for x in self.errorList:
            returnList.append("<br/>%s"%(x))

    return ''.join(returnList)