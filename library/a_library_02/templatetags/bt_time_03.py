# *********************************************************
# bt_time_03.py

## *********************************************************
from a_base_02.models import a_base_02
from django import template
from django.conf import settings
from django.template import resolve_variable
import time

register = template.Library()

modesAvailableList = ['timeSince']

# *********************************************************
class bt_time_03(template.Node):   
    
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
        if self.paramDict["MODE"] in modesAvailableList:
            if self.paramDict["MODE"] == "timeSince":
                timeDiff = time.time() - self.paramDict['OBJECT']
                if   timeDiff < 1:          returnList.append("%3.0f milliseconds ago"      % (timeDiff*1000))             
                elif timeDiff < 2:          returnList.append("1 second ago")             
                elif timeDiff < 60:         returnList.append("%d seconds ago"              % (timeDiff))             
                elif timeDiff < 120:        returnList.append("1 minute ago")             
                elif timeDiff < 3600:       returnList.append("%d minutes ago"              % (timeDiff/60))             
                elif timeDiff < 7200:       returnList.append("1 hour ago")             
                elif timeDiff < 86400:      returnList.append("%d hours ago"                % (timeDiff/3600))             
                elif timeDiff < 172800:     returnList.append("1 day ago")             
                else:                       returnList.append("%d days ago"                 % (timeDiff/86400))             
        else:
            outText = "Unknown mode (%s). Available modes are: %s" % (self.paramDict['MODE'], ', '.join(modesAvailableList))
            self.errorList.append(outText)
        # -----------------------------------------------------
             
        if settings.DEBUG:
            for x in self.errorList:
                returnList.append("<br/>%s"%(x))

        return ''.join(returnList)
