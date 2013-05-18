# *********************************************************
# a_update_02/models.py

# *********************************************************
from django.db import models
from django.forms import ModelForm
from a_base_02.models import a_base_02
from django import forms
        
# *********************************************************
class a_update_02(a_base_02):
    pass
    
    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.note)
    def get_absolute_url(self):     return "/a_update_02/%i/" % self.id
    def save(self, **kwargs):       super(a_update_02, self).save(**kwargs)   
    def delete(self, **kwargs):     super(a_update_02, self).delete(**kwargs)

    # -----------------------------------------------------
    def entryInit_c_nav_02_menu(cls):
        menuDict = []  
        menuDict.append({
                            'displayText'                           :   'update',
                            'menu'                                  :   'SIDE',
                            'view'                                  :   'a_update_02_VIEW_List',
                            'priority'                              :   3,
                            'isLocal'                               :   False,
                            'parentViewList'                        :   [],
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   [],
                            'renderMethod'                          :   '',
                            'criteriaMethod'                        :   '',
                       })  
        menuDict.append({
                            'displayText'                           :   'Dump DB -> JSON',
                            'menu'                                  :   'SIDE_LOCAL',
                            'view'                                  :   'a_update_02_VIEW_Add',
                            'priority'                              :   2,
                            'isLocal'                               :   True,
                            'parentViewList'                        :   ['a_update_02_VIEW_List'],
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   '',
                            'renderMethod'                          :   '',
                            'criteriaMethod'                        :   '',
                       })  
        return menuDict 
    entryInit_c_nav_02_menu = classmethod(entryInit_c_nav_02_menu)          

    # -----------------------------------------------------
    def viewSecurityLookupMethod(viewName):
        from a_base_02.models import secDict
        local_ViewDict = {}
        local_ViewDict['a_update_02_VIEW_List']      = secDict['s_developer']    # s_guest
        local_ViewDict['a_update_02_VIEW_Add']       = secDict['s_developer']    # s_developer
        local_ViewDict['a_update_02_VIEW_ResetTo']   = secDict['s_developer']
        local_ViewDict['a_update_02_VIEW_Contents']  = secDict['s_developer']
        
        if viewName not in local_ViewDict: return secDict['s_undefined']
        else:                                      return local_ViewDict[viewName]  
    viewSecurityLookupMethod = staticmethod(viewSecurityLookupMethod)

# *********************************************************
class Form_a_update_02(ModelForm):
    def __init__(self, *args, **kwargs): 
        super(Form_a_update_02, self).__init__(*args, **kwargs)
        
        # Common width in characters for all TextInput
        TextInputSize  = 67     
        
        # Note: using form (rather then model) input form method and widget for a field that doesn't exist in the model
        fieldName = 'note'
        self.fields[fieldName] = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size':TextInputSize,'maxlength':128,}))        

    class Meta:
        model = a_update_02
        fields = (
                    'note',
                 )    
