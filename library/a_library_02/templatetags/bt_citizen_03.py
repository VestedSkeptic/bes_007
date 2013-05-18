# *********************************************************
# bt_citizen_03.py

## *********************************************************
from a_base_02.models import a_base_02
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import resolve_variable

register = template.Library()

# *********************************************************
class bt_citizenBase_03(template.Node):   
    
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
    def get_name(self, request, citizen):
        nameResultDict = {'name':'', 'isfriend': False, 'isuser': False}
        if request.META['duo_citizen']:
            if request.META['duo_citizen'].id == citizen.id:
                nameResultDict['name']     = citizen.name
                nameResultDict['isuser']   = True
            elif citizen.id in request.META['friendsIDlist']:     
                nameResultDict['name']     = citizen.name
                nameResultDict['isfriend'] = True
            else:                          
                # Since I'm now always displaying a citizen's full name I have commented out the old code and added a new line                     
                nameResultDict['name']     = citizen.name
#                nameResultDict['name']     = citizen.direct.username
        else:                                                   
            # Since I'm now always displaying a citizen's full name I have commented out the old code and added a new line                     
            nameResultDict['name']     = citizen.name
#            nameResultDict['name'] = citizen.direct.username
        return nameResultDict

# *********************************************************
class bt_citizen_03(bt_citizenBase_03):   
    
    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        super(bt_citizen_03, self).__init__(paramDict, errorList, resolveDict)
        self.requiredParam  = ["OBJECT"]
        
    # *********************************************************
    def render(self, context):
        self.returnList     = []
        request = resolve_variable('request', context)              # Get the request variable from the context
        self.preRender_processing(context)
        
        # -----------------------------------------------------
        nameresultdict = self.get_name(request, self.paramDict["OBJECT"])
        
        if 'MODE' in self.paramDict and self.paramDict["MODE"] == 'noformat':   
            self.returnList.append(nameresultdict['name'])
        else:                                                                   
            if   nameresultdict['isuser']:      self.returnList.append(''.join(['<span class="mmh-isuser">',   nameresultdict['name'], '</span>']))   
            elif nameresultdict['isfriend']:    self.returnList.append(''.join(['<span class="mmh-isfriend">', nameresultdict['name'], '</span>']))   
            else:                               self.returnList.append(''.join(['<span class="mmh-citizen">',  nameresultdict['name'], '</span>']))   
        # -----------------------------------------------------
                  
        self.postRender_processing()
        return ''.join(self.returnList)

# *********************************************************
class bt_citizenLink_03(bt_citizenBase_03):   
    
    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        super(bt_citizenLink_03, self).__init__(paramDict, errorList, resolveDict)
        self.requiredParam  = ["OBJECT"]
        
    # *********************************************************
    def render(self, context):
        self.returnList     = []
        request = resolve_variable('request', context)              # Get the request variable from the context
        self.preRender_processing(context)
        
        # -----------------------------------------------------
        nameresultdict = self.get_name(request, self.paramDict["OBJECT"])
        
        # Hack to remove link to detail view of user for now
#        link = "<a href='%s'>%s</a>" % (reverse('a_citizen_02_VIEW_Detail', kwargs = {'object_id':self.paramDict["OBJECT"].id}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), nameresultdict['name'])
        link = "%s" % (nameresultdict['name'])
        
        if 'MODE' in self.paramDict and self.paramDict["MODE"] == 'noformat':
            self.returnList.append(link)
        else:             
            if   nameresultdict['isuser']:      self.returnList.append(''.join(['<span class="mmh-isuser">',   link, '</span>']))
            elif nameresultdict['isfriend']:    self.returnList.append(''.join(['<span class="mmh-isfriend">', link, '</span>']))
            else:                               self.returnList.append(''.join(['<span class="mmh-citizen">',  link, '</span>']))
        # -----------------------------------------------------
             
        self.postRender_processing()
        return ''.join(self.returnList)

# *********************************************************
class bt_autoCitizenLink_03(bt_citizenBase_03):   
    
    # *********************************************************
    def __init__(self, paramDict, errorList, resolveDict):
        super(bt_autoCitizenLink_03, self).__init__(paramDict, errorList, resolveDict)
        self.requiredParam  = ["OBJECT"]
        
    # *********************************************************
    def render(self, context):
        self.returnList     = []
        request = resolve_variable('request', context)              # Get the request variable from the context
        self.preRender_processing(context)
        
        # -----------------------------------------------------
        nameresultdict = self.get_name(request, self.paramDict["OBJECT"].auto_citizen)
        
        # Hack to remove link to detail view of user for now
#        link = "<a href='%s'>%s</a>" % (reverse('a_citizen_02_VIEW_Detail', kwargs = {'object_id':self.paramDict["OBJECT"].auto_citizen.id}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), nameresultdict['name'])
        link = "%s" % (nameresultdict['name'])
        
        if 'MODE' in self.paramDict and self.paramDict["MODE"] == 'noformat':
            self.returnList.append(link)
        else:
            if nameresultdict['isuser']:        self.returnList.append(''.join(['<span class="mmh-isuser">',   link, '</span>']))
            elif nameresultdict['isfriend']:    self.returnList.append(''.join(['<span class="mmh-isfriend">', link, '</span>']))
            else:                               self.returnList.append(''.join(['<span class="mmh-citizen">',  link, '</span>']))
        # -----------------------------------------------------
             
        self.postRender_processing()
        return ''.join(self.returnList)
