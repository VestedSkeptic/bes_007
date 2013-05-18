# *********************************************************
# a_msgUser_02/models.py

# *********************************************************
from a_base_02.models import a_base_02
from a_citizen_02.models import a_citizen_02
from django import forms
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm
import cPickle
import settings

# *********************************************************
msg_type_choices = (
                        ('sys',     'system'),
                        ('u2d',     'user to developer'),
                        ('u2u',     'user to user'),
                   )

# *********************************************************
class a_msgUser_02(a_base_02):
    title             = models.CharField        (max_length = 100)
    type              = models.CharField        (max_length = 3)
    body              = models.TextField        (blank = True, null = True)    
    read              = models.BooleanField     (default=False)    
    toCitizen         = models.ForeignKey       (a_citizen_02)    
    auto_fields = ['auto_timeStamp', 'auto_createdByNull']     

    # -----------------------------------------------------
    def entryInit_c_nav_02_menu(cls):
        menuDict = []  
        menuDict.append({
                            'displayText'                           :   'Global Messages',
                            'menu'                                  :   'SIDE',
                            'view'                                  :   'a_msgUser_global_02_VIEW_List',
                            'priority'                              :   3,
                            'isLocal'                               :   False,
                            'parentViewList'                        :   [],
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   [],
                            'renderMethod'                          :   '',
                            'criteriaMethod'                        :   '',
                       })  
        menuDict.append({
                            'displayText'                           :   'Add Global Message',
                            'menu'                                  :   'SIDE_LOCAL',
                            'view'                                  :   'a_msgUser_global_02_VIEW_Add',
                            'priority'                              :   2,
                            'isLocal'                               :   True,
                            'parentViewList'                        :   ['a_msgUser_global_02_VIEW_List'],
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   '',
                            'renderMethod'                          :   '',
                            'criteriaMethod'                        :   '',
                       })  
# REVIEW: removed menu entries          
###        menuDict.append({
###                            'displayText'                           :   'msgUser',
###                            'menu'                                  :   'CITIZEN',
###                            'view'                                  :   'a_msgUser_02_VIEW_List',
###                            'priority'                              :   7,
###                            'isLocal'                               :   False,
###                            'parentViewList'                        :   [],
###                            'required_viewParamsList'               :   [],
###                            'altSelectOnViewList'                   :   [],
###                            'renderMethod'                          :   'msgUserRender',
###                            'criteriaMethod'                        :   'userIsCitizen',
###                       })  
        return menuDict 
    entryInit_c_nav_02_menu = classmethod(entryInit_c_nav_02_menu)  
        
    # -----------------------------------------------------
    def msgUserRender(request, view_func, view_args, view_kwargs):
        displayText = 'system messages'
        if request.META['auto_currentView'] == 'a_msgUser_02_VIEW_List':
            returnString = "<a href='%s' class='on'>%s</a>" % (reverse('a_msgUser_02_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
        else:
            if a_msgUser_02.objects.filter(toCitizen__exact=request.META['duo_citizen'], read__exact=False).count():
                returnString = "<a href='%s' id='citizenNav-attention'>%s</a>" % (reverse('a_msgUser_02_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
            else:
                returnString = "<a href='%s'>%s</a>" % (reverse('a_msgUser_02_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
        return returnString
    msgUserRender = staticmethod(msgUserRender)       

    # -----------------------------------------------------
    def viewSecurityLookupMethod(viewName):
        from a_base_02.models import secDict
        local_ViewDict = {}
        local_ViewDict['a_msgUser_02_VIEW_List']            = secDict['s_denied']
        local_ViewDict['a_msgUser_02_VIEW_Detail']          = secDict['s_developer']
        local_ViewDict['a_msgUser_02_VIEW_Delete']          = secDict['s_citPending']
        local_ViewDict['a_msgUser_02_VIEW_ToggleRead']      = secDict['s_denied']
        local_ViewDict['a_msgUser_global_02_VIEW_List']     = secDict['s_developer']
        local_ViewDict['a_msgUser_global_02_VIEW_Add']      = secDict['s_developer']
        local_ViewDict['a_msgUser_global_02_VIEW_Edit']     = secDict['s_developer']
        local_ViewDict['a_msgUser_global_02_VIEW_Delete']   = secDict['s_developer']
        local_ViewDict['a_msgUser_global_02_VIEW_Detail']   = secDict['s_developer']
        
        if viewName not in local_ViewDict: return secDict['s_undefined']
        else:                                      return local_ViewDict[viewName]  
    viewSecurityLookupMethod = staticmethod(viewSecurityLookupMethod)     

    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.name)
    def get_absolute_url(self):     return "/a_msgUser_02/%i/" % self.id
    def delete(self, **kwargs):     super(a_msgUser_02, self).delete(**kwargs)
    def save(self, **kwargs):       super(a_msgUser_02, self).save(**kwargs)   

# -----------------------------------------------------
def internalSendUserMessage(request, title, toCitizen='', body='', type=''):
    instance                = a_msgUser_02()
    instance.title          = title
    instance.body           = body
    
    if not type: type = 'sys'
    instance.type           = type
    
    if toCitizen == 'dev':  
        instance.toCitizen = a_citizen_02.objects.get(pk=settings.DEV_DIRECT_UID)
    elif toCitizen:    
        if isinstance(toCitizen, a_citizen_02): 
            instance.toCitizen = toCitizen
        else:
            tempCitizen = a_citizen_02.objects.get(pk=toCitizen)
            instance.toCitizen = tempCitizen
    else:                   
        instance.toCitizen = request.META['duo_citizen']
        
    instance.save(request=request)
    return instance

# *********************************************************
class a_msgUser_global_02(a_base_02):
    name              = models.CharField        (max_length = 100)
    comment           = models.TextField        ()
    auto_fields       = ['auto_timeStamp', 'auto_createdTimeStamp', 'auto_citizen', 'auto_createdBy'] 

    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.name)
    def get_absolute_url(self):     return "/a_msgUser_global_02/%i/" % self.id
    def delete(self, **kwargs):     super(a_msgUser_global_02, self).delete(**kwargs)
    def save(self, **kwargs):       super(a_msgUser_global_02, self).save(**kwargs)   

    # -----------------------------------------------------
    def entryInit_middlewareMethods(cls):
        mw_methods = []
        mw_methods.append([89, 'view','mw_view_global_messages'])
        return mw_methods 
    entryInit_middlewareMethods = classmethod(entryInit_middlewareMethods)      

    # -----------------------------------------------------
    def mw_view_global_messages(request, view_func, view_args, view_kwargs):
        request.META['a_msgUser_global_message_list'] = []
        QS = a_msgUser_global_02.objects.order_by('-auto_createdTimeStamp') 
        for gMsg in QS:
            request.META['a_msgUser_global_message_list'].append(gMsg.render_global_message(request))
        return None  
    mw_view_global_messages = staticmethod(mw_view_global_messages)    
        
    # -----------------------------------------------------
    def render_global_message(self, request, xtra_contextDict={}):
        contextDict={'object': self}
        for k, v in xtra_contextDict.items():
            contextDict[k] = v 
        return self.processTemplate_01(request, 'a_msgUser_02/templates/B_global_message.html', contextDict=contextDict)     

    # -----------------------------------------------------
    def render_detail(self, request, xtra_contextDict={}):
        contextDict={'object': self}
        for k, v in xtra_contextDict.items():
            contextDict[k] = v 
        return self.processTemplate_01(request, 'a_msgUser_02/templates/B_detail.html', contextDict=contextDict)     
         
# *********************************************************
class Form_a_msgUser_global_02(ModelForm):
    def __init__(self, *args, **kwargs): 
        
        super(Form_a_msgUser_global_02, self).__init__(*args, **kwargs)
        
        # Common width in characters for all TextInput
        TextInputSize  = 67     
        
        fieldName = 'name'
        self.fields[fieldName].widget = forms.TextInput(attrs={'size':TextInputSize,'maxlength':self.fields[fieldName].max_length})
        fieldName = 'comment'
        self.fields[fieldName].widget = forms.Textarea(attrs={'cols':'50','rows':'6',})

    # -----------------------------------------------------
    class Meta:
        model = a_msgUser_global_02
        fields = (
                    'name',
                    'comment',
                 )
