# *********************************************************
# bt_comment_03.py

## *********************************************************
from django import template
from django.conf import settings
from django.template import resolve_variable
from c_comment_03.views import c_comment_03_renderThread

register = template.Library()

# *********************************************************
class bt_comment_03(template.Node):   
    
    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        self.paramDict      = paramDict
        self.errorList      = errorList
        self.resolveDict    = resolveDict
        self.requiredParam  = ["OBJECT", "MODE"]
        
    # *********************************************************
    def render(self, context):
        returnList = ['']
        
        # Get the request variable from the context
        request = resolve_variable('request', context)  
        
        if settings.DEBUG:
            for param in self.requiredParam:
                if param not in self.paramDict:
                    self.errorList.append("Did not find self.requiredParam : %s" % (param))
               
        for key, value in self.resolveDict.items():
             self.paramDict[key] = value.resolve(context)

        # -----------------------------------------------------
        indent = 0
        if "INDENT" in self.paramDict:
            indent = self.paramDict['INDENT']

        returnList.append(c_comment_03_renderThread(request, self.paramDict['OBJECT'], indent, self.paramDict["MODE"]))
        # -----------------------------------------------------
        
        if settings.DEBUG:
            for x in self.errorList:
                returnList.append("<br/>%s"%(x))

        return ''.join(returnList)
