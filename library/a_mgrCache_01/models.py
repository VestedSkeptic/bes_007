# *********************************************************
# a_mgrCache_01/models.py

# *********************************************************
from django.core.cache import cache
from django.db import models
import settings

# *********************************************************
class a_mgrCache_01(models.Model):
    cacheKey = models.CharField (primary_key=True, max_length = 255)    
    
    # -----------------------------------------------------   
    def __unicode__(self):          return u'%s' % (self.cacheKey)     
    def delete(self, **kwargs):     super(a_mgrCache_01, self).delete(**kwargs)
    def save(self, **kwargs):       super(a_mgrCache_01, self).save(**kwargs)    
        
    # -----------------------------------------------------    
    def set(cacheKey, displayItem, timeOutInSeconds=settings.CACHE_TIME_IN_SECONDS):
        cache.set(cacheKey, displayItem, timeOutInSeconds)
        
        # save this cacheKey so I can find it later when I need to clear all like it
        newInstance = a_mgrCache_01()
        newInstance.cacheKey = cacheKey
        newInstance.save()
    set = staticmethod(set)
        
    # -----------------------------------------------------    
    def get(cacheKey):
        cachedItem = cache.get(cacheKey)

        if not cachedItem and settings.DEBUG: 
            print "*** a_mgrCache_01.get(): cacheKey %s not cached" % (cacheKey)
            
        return cachedItem
    get = staticmethod(get)
        
    # -----------------------------------------------------    
    def deleteLike(cacheKey):
        # get all cacheKeys like this one (i.e. starting with)
        QS = a_mgrCache_01.objects.filter(cacheKey__startswith=cacheKey)
        
        # for each delete it from cache
        for x in QS:
            cache.delete(x.cacheKey)
        
        # then delete them from a_mgrCache_01 
        QS.delete()
    deleteLike = staticmethod(deleteLike)
        
    # -----------------------------------------------------    
    def clearAll():
        QS = a_mgrCache_01.objects.all()
        
        # for each delete it from cache
        for x in QS:
            cache.delete(x.cacheKey)
        
        # then delete them from a_mgrCache_01 
        QS.delete()
    clearAll = staticmethod(clearAll)

