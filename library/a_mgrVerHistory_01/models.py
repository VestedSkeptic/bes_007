# *********************************************************
# a_mgrVerHistory_01/models.py

# *********************************************************
from django.db import models
from a_base_02.models import a_base_02
from a_citizen_02.models import a_citizen_02
import cPickle

# *********************************************************
class a_mgrVerHistory_01(a_base_02):
    citizen         = models.ForeignKey      (a_citizen_02, related_name = 'a_mgrVerHistory_01_citizen')
    timeStamp       = models.FloatField      (max_length=14)
#    deleteFlag      = models.BooleanField    (default=False)
    version         = models.IntegerField    (default=0,)
    _fields         = models.TextField       ()
    auto_fields = ['auto_content_object']     
      
    # -----------------------------------------------------
    def __unicode__(self):          return u'%s : %s' % (self.auto_content_object, self.version)
    def get_absolute_url(self):     return "/a_mgrVerHistory_01/%i/" % self.id
    def delete(self, **kwargs):     super(a_mgrVerHistory_01, self).delete(**kwargs)
    def save(self, **kwargs):       super(a_mgrVerHistory_01, self).save(**kwargs)   
    
    # -----------------------------------------------------
    def _get_fields(self):
        returnDict = {}
        if (self._fields): returnDict = cPickle.loads(self._fields.encode('ascii'))
        return returnDict
    def _set_fields(self, xDict):
        self._fields =  cPickle.dumps(xDict)
    fields = property(_get_fields, _set_fields)