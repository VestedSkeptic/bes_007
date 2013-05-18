# *********************************************************
# e_thread_03/models.py

# *********************************************************
from a_base_02.models import a_base_02
from a_citizen_02.models import a_citizen_02
from django import forms
from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm
import settings

# *********************************************************
class e_thread_03(a_base_02):
    comment           = models.TextField            ()     
    edited            = models.BooleanField         (default=False)
    auto_fields = ['auto_timeStamp','auto_createdTimeStamp','auto_citizen','auto_content_object'] 
    
    # -----------------------------------------------------
    def entryInit_c_nav_02_menu(cls):
        menuDict = []  
        menuDict.append({
                            'displayText'                           :   'msgReply',
                            'menu'                                  :   'RIGHTCOL',
                            'view'                                  :   'e_thread_03_VIEW_List',
                            'priority'                              :   9,
                            'isLocal'                               :   False,
                            'parentViewList'                        :   [],
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   [],
                            'renderMethod'                          :   'commentRepliesRender',
                            'criteriaMethod'                        :   'userIsCitizen',
                       })  
        return menuDict 
    entryInit_c_nav_02_menu = classmethod(entryInit_c_nav_02_menu)     
    
    # -----------------------------------------------------
    def commentRepliesRender(request, view_func, view_args, view_kwargs):
        displayText = 'comments'
        if request.META['auto_currentView'] == 'e_thread_03_VIEW_List':
            returnString = "<a href='%s' class='on'>%s</a>" % (reverse('e_thread_03_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
        else:
            if e_thread_replyTracking_03.objects.filter(toCitizen=request.META['duo_citizen'], read__exact=False).count():
                displayText = 'new comments'
#                returnString = "<a href='%s' id='citizenNav-attention'>%s</a>" % (reverse('e_thread_03_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
                returnString = "<span class='mmh-replyErrorText'><a href='%s'>%s</a><span>" % (reverse('e_thread_03_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
            else:
                returnString = "<a href='%s'>%s</a>" % (reverse('e_thread_03_VIEW_List', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), displayText)
        return returnString
    commentRepliesRender = staticmethod(commentRepliesRender) 

    # -----------------------------------------------------
    def viewSecurityLookupMethod(viewName):
        from a_base_02.models import secDict
        local_ViewDict = {}
        local_ViewDict['e_thread_03_VIEW_List']     = secDict['s_citizen']
        local_ViewDict['e_thread_03_VIEW_Detail']   = secDict['s_guest']
        local_ViewDict['e_thread_03_VIEW_Raw']      = secDict['s_citizen']
        local_ViewDict['e_thread_03_VIEW_BBcode']   = secDict['s_citizen']
        
        if viewName not in local_ViewDict: return secDict['s_undefined']
        else:                              return local_ViewDict[viewName]  
    viewSecurityLookupMethod = staticmethod(viewSecurityLookupMethod)

    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.comment)
    def get_absolute_url(self):     return "/e_thread_03/%i/" % self.id
    def delete(self, **kwargs):     super(e_thread_03, self).delete(**kwargs)
    def save(self, **kwargs):       super(e_thread_03, self).save(**kwargs)   
        
# *********************************************************
class Form_e_thread_03(ModelForm):
    def __init__(self, *args, **kwargs):
        
        hiddenUniqueIdentifier = kwargs['hiddenUniqueIdentifier']
        del kwargs['hiddenUniqueIdentifier']  
         
        super(Form_e_thread_03, self).__init__(*args, **kwargs)
        
        fieldName = 'comment'
        self.fields[fieldName] = forms.CharField(label=hiddenUniqueIdentifier,widget=forms.Textarea(attrs={'cols':'45','rows':'6'}))

        fieldName = 'hiddenUniqueIdentifier'
        self.fields[fieldName] = forms.CharField(initial=hiddenUniqueIdentifier, widget=forms.HiddenInput())
        
        fieldName = 'hiddenWasEdited'
        self.fields[fieldName] = forms.CharField(initial=0, widget=forms.HiddenInput())         

    class Meta:
        model = e_thread_03
        fields = (
                    'comment',
                 )           

# *********************************************************
class e_thread_replyTracking_03(a_base_02):
    post              = models.ForeignKey           (e_thread_03,  related_name = 'post')
    toCitizen         = models.ForeignKey           (a_citizen_02, related_name = 'toCitizen')
    read              = models.BooleanField         (default=False)    
    auto_fields = ['auto_createdTimeStamp','auto_citizen'] 












