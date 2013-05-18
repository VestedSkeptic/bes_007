# *********************************************************
# bt_tags_03.py

## *********************************************************
from a_base_02.models import a_base_02
from django import template
from django.conf import settings
from django.template import resolve_variable
from tagging.models import Tag

register = template.Library()

# *********************************************************
class bt_tags_03(template.Node):   
    
    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        self.paramDict      = paramDict
        self.errorList      = errorList
        self.resolveDict    = resolveDict
        self.requiredParam  = ["OBJECT"]
        
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
        # get tags for this object
        actualTags  = Tag.objects.get_for_object(self.paramDict['OBJECT'])
        
        # proceed if there are some
        if actualTags:
            returnList.append("keywords : ")   
            
            # for each tag generate a tag_url and separate these links by a comma, space
            count = 0
            for tag in actualTags:
                count += 1
                returnList.append(self.paramDict['OBJECT'].getUrl_tag(request, tag, '+'.join(tag.__str__().split())))   
                if count < len(actualTags):
                    returnList.append(", ")   
            
            # If an append param value was passed in append it to the end
            if 'APPEND' in self.paramDict:
                returnList.append(self.paramDict['APPEND'])   
        # -----------------------------------------------------
             
        if settings.DEBUG:
            for x in self.errorList:
                returnList.append("<br/>%s"%(x))

        return ''.join(returnList)
