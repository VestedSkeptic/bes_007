# *********************************************************
# d_move_02/models.py

# *********************************************************
from a_base_02.models import a_base_02
from django import forms
# from django.contrib.contenttypes.models import ContentType
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm
# from django.forms.util import ValidationError
import settings
import time
##import cPickle
##import locale



# *********************************************************
class d_move_02(a_base_02):
    laps                            = models.IntegerField    (default=0,)
    date                            = models.CharField       (max_length=12)
    date_timestamp                  = models.FloatField      (max_length=14)
    comment                         = models.CharField       (max_length=500, blank=True, null=True)
         
    # -----------------------------------------------------
    def __unicode__(self):          return u'%s' % (self.faction_module.typeName)
    def get_absolute_url(self):     return "/d_move_02/%i/" % self.id
    def delete(self, **kwargs):     super(d_move_02, self).delete(**kwargs)
    def save(self, **kwargs):       super(d_move_02, self).save(**kwargs)        
    
    # -----------------------------------------------------
    def entryInit_c_nav_02_menu(cls):
        menuDict = []  
        menuDict.append({
                            'displayText'                           :   'MOVE',
                            'menu'                                  :   'LEFTCOL',
                            'view'                                  :   'd_move_02_VIEW_home',
                            'priority'                              :   20,
                            'isLocal'                               :   False,
                            'parentViewList'                        :   [],                             
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   ['d_move_02_VIEW_entry'],
                            'renderMethod'                          :   '',
                            'criteriaMethod'                        :   '',
                       })  
        menuDict.append({
                            'displayText'                           :   'add lap',
                            'menu'                                  :   'LEFTCOL_LOCAL',
                            'view'                                  :   'd_move_02_VIEW_addLap',
                            'priority'                              :   10,
                            'isLocal'                               :   True,
                            'parentViewList'                        :   [],                             
                            'required_viewParamsList'               :   [],
                            'altSelectOnViewList'                   :   ['d_move_02_VIEW_entry'],
                            'renderMethod'                          :   '',
                            'criteriaMethod'                        :   '',
                       })  
        return menuDict 
    entryInit_c_nav_02_menu = classmethod(entryInit_c_nav_02_menu)    
    
    # -----------------------------------------------------
    def viewSecurityLookupMethod(viewName):
        from a_base_02.models import secDict
        local_ViewDict = {}
        local_ViewDict['d_move_02_VIEW_home']                       = secDict['s_guest']
        local_ViewDict['d_move_02_VIEW_addLap']                     = secDict['s_guest']
        if viewName not in local_ViewDict: return secDict['s_undefined']
        else:                              return local_ViewDict[viewName]  
    viewSecurityLookupMethod = staticmethod(viewSecurityLookupMethod)

    # -----------------------------------------------------
    def save(self, **kwargs):
        super(d_move_02, self).save(**kwargs)

    # -----------------------------------------------------
    def entryInit_sideBarMethods(cls):
        sb_methods = []   
        return sb_methods 
    entryInit_sideBarMethods = classmethod(entryInit_sideBarMethods)     
    
# *********************************************************
class Form_d_move_02(ModelForm):
    def __init__(self, *args, **kwargs): 
        if 'instanceX' in kwargs:
            del kwargs['instanceX']             
        if 'request' in kwargs:
            del kwargs['request']             

        super(Form_d_move_02, self).__init__(*args, **kwargs)
        
        # Common width in characters for all TextInput
        TextInputSize  = 67     
        
        tt = time.strftime("%Y-%m-%d")
        
        fieldName = 'laps'
        self.fields[fieldName].widget = forms.TextInput(attrs={'size':TextInputSize})
        fieldName = 'date'
        self.fields[fieldName].widget = forms.TextInput(attrs={'size':TextInputSize,'value':tt})
        fieldName = 'comment'
        self.fields[fieldName].widget = forms.TextInput(attrs={'size':TextInputSize,'maxlength':self.fields[fieldName].max_length})
        
    # -----------------------------------------------------
    class Meta:
        model = d_move_02
        fields = (
                    'laps',
                    'date',
                    'comment',
                 )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
