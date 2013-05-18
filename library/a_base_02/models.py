# *********************************************************
# a_base_02/models.py

from a_library_02 import engine_paginate, e_paginate
from a_mgrApplication_03.models_aux import registeredClassInfo
from a_mgrCache_01.models import a_mgrCache_01
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import IntegrityError, models as standard_models
from django.db.models.base import ModelBase
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, TemplateDoesNotExist
from tagging.fields import TagField
from tagging.models import Tag
from tagging.utils import LOGARITHMIC
import cPickle
import settings
import sys
import time
#from django.core.cache import cache

# *********************************************************
auto_publish_choices = (
                            ('banner_16',     'banner_16'),
                            ('sticky_16',     'sticky_16'),
                       )

# *********************************************************
# Global Security Dict
secDict = {
           's_undefined'  : {'value':0,  'name':'undefined'},
           's_denied'     : {'value':1,  'name':'denied access'},
           's_guest'      : {'value':10, 'name':'guest'},
           's_citPending' : {'value':20, 'name':'citizen pending'},
           's_citizen'    : {'value':30, 'name':'citizen'},
           's_admin'      : {'value':40, 'name':'admin'},
           's_developer'  : {'value':50, 'name':'developer'},
           's_subscribed' : {'value':98, 'name':'subscribed'},
           's_owner'      : {'value':99, 'name':'owner'},
          }

# *********************************************************
allViewSecurityDict     = {}

# *********************************************************
class a_base_02      (standard_models.Model): pass
#class a_base_02_node (standard_models.Model): pass

#### *********************************************************
#### variations on custom query manager 
#### with auto_deleteFlag
###class objects_withDeleteFlag(standard_models.Manager):
###    def get_query_set(self):
###        return super(objects_withDeleteFlag, self).get_query_set().exclude(auto_deleteFlag__exact=True)
###class objectsDeleted_withDeleteFlag(standard_models.Manager):
###    def get_query_set(self):
###        return super(objectsDeleted_withDeleteFlag, self).get_query_set().exclude(auto_deleteFlag__exact=False)
#### without auto_deleteFlag
###class objectsDeleted_withoutDeleteFlag(standard_models.Manager):
###    def get_query_set(self):
###        return super(objectsDeleted_withoutDeleteFlag, self).none()
    
# *********************************************************
def convertClassNameToBaseAndVersion(originalClassName): 
    convertedDict = {}
    convertedDict['original'] =  originalClassName
    convertedDict['baseName'] =  originalClassName[:-3]
    convertedDict['version']  =  originalClassName[-2:]
    return convertedDict    
    
# *********************************************************
def updateAttributes(attrs, name): 
    if 'auto_versioned' in attrs['auto_fields']:
        attrs['auto_fields'].remove('auto_versioned')
        attrs['auto_fields'].append('auto_citizen')
#        attrs['auto_fields'].append('auto_deleteFlag')
        attrs['auto_fields'].append('auto_timeStamp')
        attrs['auto_fields'].append('auto_createdTimeStamp')
        attrs['auto_fields'].append('auto_version')
    
    for x in attrs['auto_fields']:
        # -----------------------------------------------------
        if x == 'auto_citizen':     
            from a_citizen_02.models import a_citizen_02
            attrs['auto_citizen']         = standard_models.ForeignKey              (a_citizen_02, related_name = name+'_auto_citizen')
        # -----------------------------------------------------
        elif x == 'auto_citizenNull': 
            from a_citizen_02.models import a_citizen_02
            attrs['auto_citizen']         = standard_models.ForeignKey              (a_citizen_02, related_name = name+'_auto_citizen', blank=True, null=True)
        # -----------------------------------------------------
        elif x == 'auto_createdBy':     
            from a_citizen_02.models import a_citizen_02
            attrs['auto_createdBy']         = standard_models.ForeignKey            (a_citizen_02, related_name = name+'_auto_createdBy')
        # -----------------------------------------------------
        elif x == 'auto_createdByNull': 
            from a_citizen_02.models import a_citizen_02
            attrs['auto_createdBy']         = standard_models.ForeignKey            (a_citizen_02, related_name = name+'_auto_createdBy', blank=True, null=True)
###        # -----------------------------------------------------
###        elif x == 'auto_deleteFlag':  
###            attrs['auto_deleteFlag']      = standard_models.BooleanField            (default=False)
###            auto_deleteFlagFound = True
        # -----------------------------------------------------
        elif x == 'auto_timeStamp':  
            attrs['auto_timeStamp']       = standard_models.FloatField              (max_length=14)
        # -----------------------------------------------------
        elif x == 'auto_createdTimeStamp':  
            attrs['auto_createdTimeStamp']= standard_models.FloatField              (max_length=14)
        # -----------------------------------------------------
        elif x == 'auto_version':  
            attrs['auto_version']         = standard_models.IntegerField            (default=0,)
        # -----------------------------------------------------
#         elif x == 'auto_category':  
#             from a_mgrCategories_02.models import a_mgrCategories_02
#             attrs['auto_category']        = standard_models.ForeignKey              (a_mgrCategories_02, related_name = name+'_auto_category', blank=True, null=True)
        # -----------------------------------------------------
        elif x == 'auto_content_object':  
            attrs['auto_content_type']    = standard_models.ForeignKey              (ContentType)
            attrs['auto_object_id']       = standard_models.PositiveIntegerField    ()
            attrs['auto_content_object']  = generic.GenericForeignKey               (ct_field='auto_content_type', fk_field='auto_object_id')
        # -----------------------------------------------------
#         elif x == 'auto_publish':
#             from a_mgrPublish_02.models import a_mgrPublish_02
#             attrs['auto_publish']          = standard_models.CharField               (max_length = 9, choices=auto_publish_choices, blank=True, null=True)
#             attrs['publishKey']            = generic.GenericRelation                 (a_mgrPublish_02)
        # -----------------------------------------------------
        elif x == 'auto_geoAddress':
            auto_geoAddress_okToCreate = True
            if attrs.has_key('auto_geoFields'):
                for z in attrs['auto_geoFields']:
                    if z not in attrs:
                        auto_geoAddress_okToCreate = False
                        print "*** auto_geoAddress: auto_geoField (%s) not defined" % (z)
            else:
                auto_geoAddress_okToCreate = False
                print "*** auto_geoAddress WITHOUT associated auto_geoFields field."
            
#             if auto_geoAddress_okToCreate:
#                 from a_geoAddress_01.models import a_geoAddress_01
#                 attrs['auto_geoAddress']  = standard_models.ForeignKey      (a_geoAddress_01, related_name = name+'_auto_geoAddress', blank=True, null=True)
#                 attrs['auto_geoFields']   = attrs['auto_geoFields']   # MMH: Consider making auto_geoFields a static class property rather then an instance property since it is the same for all instances and could be reduced for lower memory usage
#             else:
#                 print "*** auto_geoAddress fields not created due to errors."
        # -----------------------------------------------------
        elif x == 'auto_urlReduced':
            if attrs.has_key('url'):  attrs[x]               = standard_models.CharField  (blank=True, max_length = 80,)    
            else:                     print "*** auto_urlReduced WITHOUT associated url field. Not creating field for auto_urlReduced."
        # -----------------------------------------------------
        elif x == 'auto_tags':
            attrs['auto_tags']     = TagField()
        # -----------------------------------------------------
        else: 
            print "*** class [%s] has unknown auto_field [%s]" % (name, x)  
    
    return attrs  

# *********************************************************
class IntermediateModelBase(ModelBase): 
    def __new__(cls, name, bases, attrs):
        
#        print "name = %s" % (name)        
#        print "bases = %s" % (bases)
        
        if bases == (a_base_02,):               # if bases == (a_base_02,) or bases == (a_base_02_node,):
            
            # Update attributes for auto_fields present
            if attrs.has_key('auto_fields'): attrs = updateAttributes(attrs, name)
               
###            # set custom model managers         
###            if auto_deleteFlagFound:
###                attrs['objects']        = objects_withDeleteFlag()
###                attrs['objectsAll']     = standard_models.Manager()
###                attrs['objectsDeleted'] = objectsDeleted_withDeleteFlag()
###            else:
###                attrs['objects']        = standard_models.Manager()
###                attrs['objectsAll']     = standard_models.Manager()
###                attrs['objectsDeleted'] = objectsDeleted_withoutDeleteFlag()

            attrs['objects']        = standard_models.Manager()
            attrs['objectsAll']     = standard_models.Manager()
                
            # ACTUALLY CREATE THE NEW CLASS
            newclass = ModelBase.__new__(ModelBase, name, (standard_models.Model,), attrs) 

            # but then make it inherit back to a_base_02 and/or a_base_02_node class as appropriate 
###            if   bases == (a_base_02_node,):   newclass.__bases__ = (a_base_02_node,  a_base_02,)
###            else:                              newclass.__bases__ = (a_base_02,)
            newclass.__bases__ = (a_base_02,)
        else: 
            newclass = type.__new__(cls, name, bases, attrs) 
            
            
        # reduce the name by removing the version + add a version
        convertedDict = convertClassNameToBaseAndVersion(newclass.__name__)
        newclass.__baseName__   = convertedDict['baseName']
        newclass.__version__    = convertedDict['version']
        
        # put class into registeredClassInfo
        registeredClassInfo.add_newEntry(newclass.__baseName__, newclass)
        
        return newclass
    
# *********************************************************
class a_base_02(standard_models.Model): # @DuplicatedSignature
    __metaclass__ = IntermediateModelBase
    
    # *****************************************************
    def entryInit_class(cls):
        if cls.__baseName__ <> 'a_base':
#            print "*** %-42s %32s - Fell through." % ('entryInit_class', cls.__baseName__)
            registeredClassInfo.set_entryUnused(cls.__baseName__, 'entryInit_class')        # track methods that fall through so I also know methods that were written for an app/component. 
        else:
            pass
    entryInit_class = classmethod(entryInit_class)      
    
    # *****************************************************
    def entryInit_middlewareMethods(cls):
        mw_methods = []
        if cls.__baseName__ <> 'a_base':
#            print "*** %-42s %32s - Fell through." % ('entryInit_middlewareMethods', cls.__baseName__)
            registeredClassInfo.set_entryUnused(cls.__baseName__, 'entryInit_middlewareMethods')    # which I can use to drive a visual display (think of it as a status panel) of applications/components installed and the code/entry points driving them.
        else:
            pass
        return mw_methods 
    entryInit_middlewareMethods = classmethod(entryInit_middlewareMethods)      
    
    # *****************************************************
    def entryInit_c_nav_02_menu(cls):
        local_MenuList = []
        if cls.__baseName__ <> 'a_base':
            #print "*** %-32s %32s - Fell through." % ('entryInit_c_nav_02_menu', cls.__baseName__)
            registeredClassInfo.set_entryUnused(cls.__baseName__, 'entryInit_c_nav_02_menu')    # track methods that fall through so I also know methods that were written for an app/component. 
        else:
            pass
        return local_MenuList 
    entryInit_c_nav_02_menu = classmethod(entryInit_c_nav_02_menu)      

    # *****************************************************
    def entryInit_dependencies(cls):
        dependsOnList = []
        if cls.__baseName__ <> 'a_base':
#            print "*** %-32s %32s - Fell through." % ('entryInit_dependencies', cls.__baseName__)
            registeredClassInfo.set_entryUnused(cls.__baseName__, 'entryInit_dependencies')    # track methods that fall through so I also know methods that were written for an app/component. 
        else:
            pass
        return dependsOnList 
    entryInit_dependencies = classmethod(entryInit_dependencies)      
    
    # *****************************************************
    def entryInit_sideBarMethods(cls):
        sb_methods = []
        if cls.__baseName__ <> 'a_base':
#            print "*** %-32s %32s - Fell through." % ('entryInit_sideBarMethods', cls.__baseName__)
            registeredClassInfo.set_entryUnused(cls.__baseName__, 'entryInit_sideBarMethods')        # track methods that fall through so I also know methods that were written for an app/component. 
        else:
            pass
        return sb_methods
    entryInit_sideBarMethods = classmethod(entryInit_sideBarMethods)      
    
    # *****************************************************
    def setSecurityForView(cls, classObj):
        try:
            import_urls   = classObj.__name__+".urls"
            try:
                urlpatterns = getattr(__import__(import_urls, {}, {}, ['urlpatterns'], -1), 'urlpatterns')   
                try:
                    viewSecurityLookupMethod = getattr(classObj, 'viewSecurityLookupMethod')
                    
                    for x in urlpatterns:
                        if x.callback.__name__ not in allViewSecurityDict:
                            allViewSecurityDict[x.callback.__name__] = [viewSecurityLookupMethod(x.callback.__name__), classObj]
                            
                except AttributeError, e:
                    print "++= AttributeError: %s" % (e)
            except AttributeError, e:
                pass
        except ImportError, e:
            pass
    setSecurityForView = classmethod(setSecurityForView)      
    
    # *****************************************************
    def reviewSecurityForAllView(cls, classObj):
        # finally check that no entries were set to undefined which would mean
        # viewName wasn't found in the class specific viewSecurityLookupMethod
        for k, v in allViewSecurityDict.items():
            if v[0]['name'] == 'undefined':
                print "*** reviewSecurityForAllView error: undefined for %s" % (k)    
    reviewSecurityForAllView = classmethod(reviewSecurityForAllView)

    # *****************************************************
    def mw_request_applicationInitialization_calledOnce(request):
        from a_mgrMiddleWare_02.models  import a_mgrMiddleWare_02
        from a_mgrApplication_03.models import componentInstalled
        from a_mgrSidebar_02.models     import a_mgrSidebar_02
        from a_mgrCache_01.models       import a_mgrCache_01

        a_mgrCache_01.clearAll()

        registeredClassInfo.clear_internalRegisteredClassesDict()
        
        # ======================================
        for x in settings.INSTALLED_APPS:
            if x[:6] <> 'django': 
                # import the file
                import_file   = x+".models"
                __import__(import_file, {}, {}, [], -1)
                
                # call init on the class
                getattr(x, '__init__')()        
        # ======================================
        
        lastClassObject = ""        # Finding the last classInfo.classObject to be used below to call reviewSecurityForAllView
        
        # Restructured this to run through the for loop twice because on webfaction released version
        # I would occasionally get an error with the code in the second forloop iteration just added. 
        # I think that was because of an arbitrary initialization order
        for name, classInfo in registeredClassInfo.get_items():
            classInfo.classObject.entryInit_class()
       
        for name, classInfo in registeredClassInfo.get_items():
            a_mgrMiddleWare_02.register_middlewareMethods(classInfo.classObject.entryInit_middlewareMethods(), classInfo.classObject.__baseName__)
            
            classInfo.classObject.setSecurityForView(classInfo.classObject)
            lastClassObject = classInfo.classObject

            if componentInstalled('c_nav'):
                classInfo.get_classObject_fromBaseName('c_nav').register_c_nav_02_menuItems  (request, classInfo.classObject.entryInit_c_nav_02_menu(),     classInfo.classObject.__baseName__)

            a_mgrSidebar_02.register_sidebarMethods(classInfo.classObject.entryInit_sideBarMethods(), classInfo.classObject.__baseName__)
                
        if lastClassObject:
            lastClassObject.reviewSecurityForAllView(lastClassObject)
            
        a_mgrMiddleWare_02.mwDelMethod(1, 'request', 'a_base', 'mw_request_applicationInitialization_calledOnce')
        return None    
    mw_request_applicationInitialization_calledOnce = staticmethod(mw_request_applicationInitialization_calledOnce)      
    
    # *****************************************************
    def __init__(self, *args, **kwargs): 
        super(a_base_02, self).__init__(*args, **kwargs)
        if self.__dict__.has_key('auto_category_id'):
            if self.auto_category:
                self.inital_auto_category = self.auto_category
        
    # *****************************************************
    def save(self, **kwargs):
        timeNow = time.time()
        
        if self.__dict__.has_key('auto_category_id'):
            initial_category = ''
            if self.__dict__.has_key('inital_auto_category'):
                initial_category = self.inital_auto_category
            
            if initial_category <> self.auto_category:
                if initial_category: 
                    initial_category.dec_appCount(self.__class__.__name__)
                    initial_category.save(request=kwargs['request'])
                self.auto_category.inc_appCount(self.__class__.__name__)
                self.auto_category.save(request=kwargs['request'])
                
        if self.__dict__.has_key('auto_version'):
            self.auto_version += 1
            
        if self.__dict__.has_key('auto_timeStamp'):
            self.auto_timeStamp = timeNow
            
        if self.__dict__.has_key('auto_createdTimeStamp') and not self.auto_createdTimeStamp:
            self.auto_createdTimeStamp = timeNow

        if self.__dict__.has_key('auto_citizen_id'):
            if 'request' in kwargs:    
                self.auto_citizen = kwargs['request'].META['duo_citizen']
            else:                      
                raise Exception, "Error: auto_citizen class saved without request instance"

        if self.__dict__.has_key('auto_createdBy_id') and not self.auto_createdBy_id:
            if 'request' in kwargs:    
                self.auto_createdBy = kwargs['request'].META['duo_citizen']
            else:                      
                raise Exception, "Error: auto_version class saved without request instance"
            
        if self.__dict__.has_key('auto_urlReduced'):
            if self.url:
                urlWithoutHTTP = self.url.split("//",1)                # a. remove pre http://
                reducedUrlList = urlWithoutHTTP[1].split("/",1)        # b. remove post /etc.
                self.auto_urlReduced = reducedUrlList[0]
                if self.auto_urlReduced.find('www.') <> -1:            # c. remove www. if exists
                    self.auto_urlReduced = self.auto_urlReduced.split("www.",1)[1]

        if self.__dict__.has_key('_auto_tags_cache'):
            # clean the tags by 
            # 1) splitting and recombining by whitespace to remove any extra spaces
            # 2) strip whitespace from beginning and end
            x = ' '.join(self._auto_tags_cache.split()).strip()
            self._auto_tags_cache = x
        
        # PERFORM THE ACTUAL SAVE
        super(a_base_02, self).save()    
        # PERFORM THE ACTUAL SAVE

        if self.__dict__.has_key('auto_version'):
            # MMH: If this instance is deleted I should consider deleting all the auto_version instances associated with it.
            # See delete of associated auto_publish items for example
            from a_mgrVerHistory_01.models import a_mgrVerHistory_01
            
            version                     = a_mgrVerHistory_01()
            version.citizen             = self.auto_citizen 
            version.timeStamp           = timeNow
#            version.deleteFlag          = self.auto_deleteFlag
            version.auto_content_object = self
            version.version             = self.auto_version
            
            fieldsDict = {}
            for k, v in self.__dict__.items():
                # Strip out some fields which are never saved with version info
                fieldOkToArchive = True
                # to remove django field such as '_auto_citizen_cache' which are internally used for foreign keys
                if k[0]=='_' and k[-6:] == '_cache': fieldOkToArchive = False   # mmh: use a regular expression to speed this up
                if fieldOkToArchive: fieldsDict[k] = v
            version.fields        = fieldsDict 
            version.save()                   

        # process geolocation of auto_geoAdd in a signal
        # because save triggers a thread we have to we have to check 'fromThread' in kwargs to avoid an infinate loop when using save from a thread
#         if self.__dict__.has_key('auto_geoAddress_id'):
#             if 'fromThread' not in kwargs:
#                 from django.dispatch import dispatcher
#                 from a_library_02 import engine_signals                
#                 
#                 addressChunkList = []
#                 for x in self.auto_geoFields:
#                     if self.__dict__[x]:
#                         addressChunkList.append([x, self.__dict__[x]])
#         
#                 engine_signals.geoLocateAddressSignal.connect(
#                                    engine_signals.process_geoLocateAddressSignal, 
#                                    ) 
#                 engine_signals.geoLocateAddressSignal.send(
#                                 instance         = self, 
#                                 addressChunkList = addressChunkList, 
#                                 request          = kwargs['request'],
#                                 sender  = None,                                
#                                 )  

#         if self.__dict__.has_key('auto_publish'):
#             from a_mgrPublish_02.models import a_mgrPublish_02
#             if self.auto_publish:
#                 try:
#                     inst_type = ContentType.objects.get_for_model(self)
#                     publish_inst = a_mgrPublish_02.objects.get(content_type__pk=inst_type.id, object_id=self.id)
#                     publish_inst.publishMode = self.auto_publish
#                     publish_inst.save(request=kwargs['request'])
#                 except ObjectDoesNotExist:
#                     publish_inst = a_mgrPublish_02()
#                     publish_inst.content_object = self
#                     publish_inst.publishMode = self.auto_publish
#                     publish_inst.save(request=kwargs['request']) 
#             else:
#                 try:
#                     inst_type = ContentType.objects.get_for_model(self)
#                     publish_inst = a_mgrPublish_02.objects.get(content_type__pk=inst_type.id, object_id=self.id)
#                     publish_inst.delete(request=kwargs['request'])
#                 except ObjectDoesNotExist:
#                     pass
            
    # *****************************************************
    def delete(self, **kwargs):
#        if self.__dict__.has_key('auto_deleteFlag'):
#            if not self.auto_deleteFlag:     # first delete is to set deleteFlag to true
#                self.auto_deleteFlag = True
#                self.save(**kwargs)
#                return

        if self.__dict__.has_key('auto_category_id'):
            self.auto_category.dec_appCount(self.__class__.__name__)
            self.auto_category.save(request=kwargs['request'])            
        
#         # Delete associated auto_publish instance if it exists
#         if self.__dict__.has_key('auto_publish'):
#             from a_mgrPublish_02.models import a_mgrPublish_02
#             try:
#                 inst_type = ContentType.objects.get_for_model(self)
#                 instance = a_mgrPublish_02.objects.get(content_type__pk=inst_type.id, object_id=self.id)
# #                print "*** Deleting associated auto_publish instance %s" % (instance)
#                 instance.delete(request=kwargs['request'])
#             except ObjectDoesNotExist:
# #                print "*** No associated auto_publish instance to delete"
#                 pass
        
        super(a_base_02, self).delete()
        
    # *****************************************************
    def setTitle(request, title_text = ''):
        titleList = []
#        titleList.append("besomeone.ca")
        
        if not title_text:
            title_text = "%s - %s" % (settings.SITE_NAME, request.META['auto_currentView'])

        titleList.append(title_text)
            
        request.META['bes_title'] = ' - '.join(titleList).lower()
    setTitle = staticmethod(setTitle)
        
    # *****************************************************
    def GET_publishTimeStamp(self):
        rvalue = 0
        if self.__dict__.has_key('auto_publish'):
            QS = self.publishKey.all()
            for x in QS:
                rvalue = x.auto_createdTimeStamp
        return rvalue
        
    # *****************************************************
    def webafiedText(self, stringX):
        stringX = stringX.replace('\n','<br/>')
        stringX = stringX.replace(' ','&nbsp;')
        return stringX
        
    # *****************************************************
    # simply a wrapper around a_mgrEmail_02.queueAndSend
    def sendEmailEWrapper(request, subject, toList, bodyTemplate='', bodyContextDict={}, bodyText=''):
        from a_mgrEmail_02.models import a_mgrEmail_02  
        a_mgrEmail_02.queueAndSend(request, subject, toList, bodyTemplate=bodyTemplate, bodyContextDict=bodyContextDict, bodyText=bodyText)  
    sendEmailEWrapper = staticmethod(sendEmailEWrapper)
        
    # *****************************************************
    # simply a wrapper around a_msgSocial_02.internalQueueSocialMessage
    def queueSocialMessage(messageName, kwargs, request, destination='', priority='',):
        from a_msgSocial_02.models import internalQueueSocialMessage  
        return internalQueueSocialMessage(messageName, kwargs, request, destination, priority)      
    queueSocialMessage = staticmethod(queueSocialMessage)
        
    # *****************************************************
    # simply a wrapper around a_msgUser_02.internalSendUserMessage
    def sendUserMessage(request, title, toCitizen='', body='', type=''):
        from a_msgUser_02.models import internalSendUserMessage  
        return internalSendUserMessage(request, title, toCitizen, body, type)
    sendUserMessage = staticmethod(sendUserMessage)
        
    # *****************************************************
    def get_tagcloud_objects(cls, steps=settings.TAGCLOUD_STEPS, distribution=LOGARITHMIC, filters=None, min_count=settings.TAGCLOUD_MINCOUNT):
        model = registeredClassInfo.get_classObject_fromBaseName(cls.__baseName__)
        return Tag.objects.cloud_for_model(model, steps=steps, distribution=distribution, filters=filters, min_count=min_count)
    get_tagcloud_objects = classmethod(get_tagcloud_objects)
        
    # *****************************************************
    def get_tagcloud_linklist(request, tagcloud_objects, tagView, tag='', kwargsDict={}):
        tagcloudLinkList = []
        
        for y in tagcloud_objects:
            combinedName = '+'.join(y.name.split())
            
            if hasattr(y, 'font_size'):
                if combinedName == tag:   
#                    tagcloudLinkList.append("&nbsp;<font size ='%s' class='mmh-set02'>%s</font>" % (y.font_size, y.name))
#                    tagcloudLinkList.append("&nbsp;<font class='mmh-set02'>%s</font>" % (y.name))
                    tagcloudLinkList.append("&nbsp;%s" % (y.name))
                else:      
                    kwargsDict['tag'] = combinedName
#                    tagcloudLinkList.append("&nbsp;<font size ='%s'><a href='%s'>%s</a></font>" % (y.font_size, reverse(tagView, kwargs = kwargsDict, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), y.name))
#                    tagcloudLinkList.append("&nbsp;<font><a href='%s'>%s</a></font>" % (reverse(tagView, kwargs = kwargsDict, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), y.name))
                    tagcloudLinkList.append("&nbsp;<a href='%s'>%s</a>" % (reverse(tagView, kwargs = kwargsDict, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)), y.name))
            else:
                tagcloudLinkList.append("&nbsp;(%s)" % (y.name))
        return tagcloudLinkList
    get_tagcloud_linklist = staticmethod(get_tagcloud_linklist)
        
    # *****************************************************
    def getCached_tagCloud(cls, request, tag, viewName, filter, title, kwargsDict={}):
        model       = registeredClassInfo.get_classObject_fromBaseName(cls.__baseName__)
        baseTag     = 'tagCloud'
        
        if tag:     
            if kwargsDict:  cacheKey    = '-'.join([cls.__baseName__, baseTag, '-'.join(kwargsDict.values()), tag])
            else:           cacheKey    = '-'.join([cls.__baseName__, baseTag, tag])
        else:       
            if kwargsDict:  cacheKey    = '-'.join([cls.__baseName__, baseTag, '-'.join(kwargsDict.values())])
            else:           cacheKey    = '-'.join([cls.__baseName__, baseTag])
            
        displayItem = a_mgrCache_01.get(cacheKey)

        if not displayItem:
            tagcloud_objects    = model.get_tagcloud_objects(filters=filter)
            if tagcloud_objects:
#                print "THERE ARE SOME tagcloud_objects"
                tagcloud_linklist   = model.get_tagcloud_linklist(request, tagcloud_objects, viewName, tag, kwargsDict)
                displayItem = model.processTemplate_01(request, 'B_tagcloud.html', {'tagcloud': tagcloud_linklist,'title':title})
            else:
#                print "THERE ARE NO tagcloud_objects"
                displayItem = ''      
            a_mgrCache_01.set(cacheKey, displayItem)
        return displayItem
    getCached_tagCloud = classmethod(getCached_tagCloud)
        
    # *****************************************************
    def clearCached_tagCloud(cls, kwargsDict={}):
        model       = registeredClassInfo.get_classObject_fromBaseName(cls.__baseName__)
        baseTag     = 'tagCloud'
        
        if kwargsDict:  cacheKey    = '-'.join([cls.__baseName__, baseTag, '-'.join(kwargsDict.values())])
        else:           cacheKey    = '-'.join([cls.__baseName__, baseTag])
        
        a_mgrCache_01.deleteLike(cacheKey)
    clearCached_tagCloud = classmethod(clearCached_tagCloud)
        
    # *****************************************************
    def getCached_externalLinkList(cls, request, title='External Links'):
        model       = registeredClassInfo.get_classObject_fromBaseName(cls.__baseName__)
        baseTag     = 'externalLinkList'

        cacheKey    = '-'.join([cls.__baseName__, baseTag])
        displayItem = a_mgrCache_01.get(cacheKey)
        
        if not displayItem:
            listOfLinks = []
    
            QS = model.objects.values_list('auto_urlReduced', flat=True).distinct()         
            for x in QS:
                if x:
                    listOfLinks.append(x)
                    
            if listOfLinks:
                listOfLinks.sort()
                displayItem = a_base_02.processTemplate_01(request, 'B_externalLinkList.html', {'listOfLinks': listOfLinks, 'title':title})
            else:
                displayItem = ''
            a_mgrCache_01.set(cacheKey, displayItem)
        return displayItem
    getCached_externalLinkList = classmethod(getCached_externalLinkList)
        
    # *****************************************************
    def clearCached_externalLinkList(cls):
        model       = registeredClassInfo.get_classObject_fromBaseName(cls.__baseName__)
        baseTag     = 'externalLinkList'
        
        cacheKey    = '-'.join([cls.__baseName__, baseTag])
        a_mgrCache_01.deleteLike(cacheKey)
    clearCached_externalLinkList = classmethod(clearCached_externalLinkList)
        
    # *****************************************************
    def auto_detail(request, object_id, baseHTML='BASE.html', vTitle='', template='BLOCK_Detail'):
        try:
            contextDict = {}
            obj2detail = registeredClassInfo.get_classObject_fromBaseName(request.META['auto_currentApp_baseName']).objectsAll.get(pk=object_id)
            contextDict['vTitle'] = vTitle
            contextDict['main_1'] = a_base_02.processTemplate_01(request, ''.join([request.META['auto_currentApp'],'/templates/',template,'.html']), {'object': obj2detail})
            return a_base_02.processTemplate_01(request, baseHTML, contextDict, mode='view')    
        except  ObjectDoesNotExist:
            raise Http404
    auto_detail = staticmethod(auto_detail)
        
    # *****************************************************
    # This version uses the classname instead of auto_currentApp_baseName and auto_currentApp
    # converted by adding cls as first parameter
    # converted by changing it from a staticmethod to a class method
    def auto_detail_02(cls, request, object_id, baseHTML='BASE.html', vTitle='', template='BLOCK_Detail'):
        convertedDict = convertClassNameToBaseAndVersion(cls.__name__)
        
#        print "convertedDict['baseName'] = %s" % (convertedDict['baseName'])
#        print "request.META['auto_currentApp']             = %s" % (request.META['auto_currentApp'])
#        print "request.META['auto_currentView']            = %s" % (request.META['auto_currentView'])
#        print "request.META['auto_currentApp_baseName']    = %s" % (request.META['auto_currentApp_baseName'])
#        print "request.META['auto_currentApp_version']     = %s" % (request.META['auto_currentApp_version'])
        
        try:
            contextDict = {}
            obj2detail = registeredClassInfo.get_classObject_fromBaseName(convertedDict['baseName']).objectsAll.get(pk=object_id)
            
            contextDict['vTitle'] = vTitle
            contextDict['main_1'] = a_base_02.processTemplate_01(request, ''.join([request.META['auto_currentApp'],'/templates/',template,'.html']), {'object': obj2detail})
            return a_base_02.processTemplate_01(request, baseHTML, contextDict, mode='view')    
        except  ObjectDoesNotExist:
            raise Http404
    auto_detail_02 = classmethod(auto_detail_02)
        
    # *****************************************************
    def auto_publishItem(request, appName, object_id, publishMode):
        try:
            contextDict = {}
            obj2publish = registeredClassInfo.get_classObject_fromBaseName(appName).objectsAll.get(pk=object_id)
            templateList = [obj2publish.__class__.__name__, '/templates/PUBLISH_', publishMode, '.html']
            try:
                return a_base_02.processTemplate_01(request, ''.join(templateList), {'object': obj2publish})
            except TemplateDoesNotExist:
                if settings.DEBUG: print "*** ERROR: template %s does not exist" % (''.join(templateList))
        except  ObjectDoesNotExist:
            if settings.DEBUG: print "*** ERROR: auto_publishItem (id = %s) does not exist" % (object_id)

    auto_publishItem = staticmethod(auto_publishItem)
        
    # *****************************************************
    def auto_list(request, objectList, sortBy=[], extraContextDict={}, paginateBy='', baseHTML='BASE.html', vTitle='', template='BLOCK_List'):
        contextDict = {}
        if not paginateBy: paginateBy = 10
        
        if objectList:
            sortDict = {}
            
            pg = engine_paginate.engine_paginate(request, objectList, request.META['auto_currentApp'], sortBy=sortBy, paginateBy=paginateBy) 
            if pg.paginatedListFound:
                contextDict.update(dict(
                                    paginatedListFound = True,
                                    page_first         = pg.first_url(),
                                    page_last          = pg.last_url(),
                                    page_previous      = pg.previous_url(),
                                    page_next          = pg.next_url(), 
                                    ))
            
            extraContextDict['objectList']   = pg.objectList  
            
            if len(sortBy): 
                extraContextDict['sortDict']     = pg.get_sortByNavigationDict()   
            
            contextDict['vTitle'] = vTitle
            contextDict['main_1'] = a_base_02.processTemplate_01(request, ''.join([request.META['auto_currentApp'],'/templates/',template,'.html']), extraContextDict)    
        else:
            contextDict['vTitle'] = vTitle
            contextDict['main_1'] = 'There are no items to display here.'
            
        return a_base_02.processTemplate_01(request, baseHTML, contextDict, mode='view')   
    auto_list = staticmethod(auto_list)
        
    # *****************************************************
    def auto_delete(request, object_id, confirm='', baseHTML='BASE.html', vTitle=''):
        try:
            obj2delete = registeredClassInfo.get_classObject_fromBaseName(request.META['auto_currentApp_baseName']).objectsAll.get(pk=object_id)
            if not confirm:
                contextDict = {}
                confirmDict = { 'object'          : obj2delete,
                                'yesLink'         : reverse(request.META['auto_currentApp']+'_VIEW_DeleteConfirm', kwargs = {'object_id':object_id,'confirm':'yes'}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)),
                                'noLink'          : reverse(request.META['auto_currentApp']+'_VIEW_DeleteConfirm', kwargs = {'object_id':object_id,'confirm':'no'}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)),
                                'detailTemplate'  : request.META['auto_currentApp']+'/templates/BLOCK_Detail.html',
                                'deleteConfirm'   : 1,
                               }
                contextDict['vTitle'] = vTitle                
                contextDict['main_1'] = a_base_02.processTemplate_01(request, 'BLOCK_ConfirmDelete.html', confirmDict)
                return a_base_02.processTemplate_01(request, baseHTML, contextDict, mode='view')
            elif confirm=='yes':
                obj2delete.delete(request=request)
                return a_base_02.redirectView(request, request.META['auto_currentApp']+'_VIEW_List', 'delete')    
            else:
                return a_base_02.redirectView(request, request.META['auto_currentApp']+'_VIEW_List', 'deleteU')     
        except  ObjectDoesNotExist:            
            raise Http404
    auto_delete = staticmethod(auto_delete)
    
    # *****************************************************
    # This version uses the classname instead of auto_currentApp_baseName and auto_currentApp
    # converted by adding cls as first parameter
    # converted by changing it from a staticmethod to a class method
    def auto_delete_02(cls, request, object_id, confirm='', baseHTML='BASE.html', vTitle='', template='BLOCK_Detail'):
        convertedDict = convertClassNameToBaseAndVersion(cls.__name__)
        try:
            obj2delete = registeredClassInfo.get_classObject_fromBaseName(convertedDict['baseName']).objectsAll.get(pk=object_id)
            if not confirm:
                contextDict = {}
                confirmDict = { 'object'          : obj2delete,
                                'yesLink'         : reverse(cls.__name__+'_VIEW_DeleteConfirm', kwargs = {'object_id':object_id,'confirm':'yes'}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)),
                                'noLink'          : reverse(cls.__name__+'_VIEW_DeleteConfirm', kwargs = {'object_id':object_id,'confirm':'no'},  urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)),
                                'detailTemplate'  : ''.join([request.META['auto_currentApp'],'/templates/',template,'.html']),
                                'deleteConfirm'   : 1,
                               }
                contextDict['vTitle'] = vTitle                
                contextDict['main_1'] = a_base_02.processTemplate_01(request, 'BLOCK_ConfirmDelete.html', confirmDict)
                return a_base_02.processTemplate_01(request, baseHTML, contextDict, mode='view')
            elif confirm=='yes':
                obj2delete.delete(request=request)
                return a_base_02.redirectView(request, cls.__name__+'_VIEW_List', 'delete')    
            else:
                return a_base_02.redirectView(request, cls.__name__+'_VIEW_List', 'deleteU')     
        except  ObjectDoesNotExist:            
            raise Http404
    auto_delete_02 = classmethod(auto_delete_02)
        
    # *****************************************************
    def processTemplate_01(request, templateName, contextDict=None, mode='block'):
        context  = RequestContext(request)
        template = loader.get_template(templateName)
        
        if contextDict is None: contextDict = {}
        for key, value in contextDict.items():
            if callable(value): context[key] = value()
            else:               context[key] = value
            
        if mode == 'block': return template.render(context)
        else:               return HttpResponse(template.render(context), mimetype=None)     
    processTemplate_01 = staticmethod(processTemplate_01)    
        
    # *****************************************************
    def processTemplate_02_withPagination(request, templateName, contextDict=None, contextPaginationKey='', mode='block'):
        context  = RequestContext(request)
        template = loader.get_template(templateName)
        
        if contextDict is None: 
            contextDict = {}
        elif contextPaginationKey:
            pg = e_paginate.e_paginate(request, contextDict, contextPaginationKey) 
            if pg.paginatedListFound:
                contextDict.update(dict(
                                    paginatedListFound = True,
                                    page_first         = pg.first_url(),
                                    page_last          = pg.last_url(),
                                    page_previous      = pg.previous_url(),
                                    page_next          = pg.next_url(), 
                                    ))
            contextDict[contextPaginationKey]   = pg.objectList  
            
        for key, value in contextDict.items():
            if callable(value): context[key] = value()
            else:               context[key] = value
            
        if mode == 'block': return template.render(context)
        else:               return HttpResponse(template.render(context), mimetype=None)     
    processTemplate_02_withPagination = staticmethod(processTemplate_02_withPagination)    

    # *****************************************************
    def redirectView(request, viewName, reason, kwargs={}):
##        from a_mgrVerHistory_01.models import redirect_reason_Choices
##        
##        reasonFound = True
##        if settings.DEBUG:
##            reasonFound = False
##            for x in redirect_reason_Choices:
##                if reason == x[0]:
##                    reasonFound = True
##                    break
##            if not reasonFound:
##                print "*** reason %s NOT FOUND IN redirect_reason_Choices" % (reason)
##                reason = 'invalid'
          
        request.session['redirect_rational'] = reason
        
        if reason == 'menu_navF': return request.facebook.redirect(request.META['duo_FormActionPrepend']+reverse(viewName, kwargs=kwargs, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)))
        else:                     return HttpResponseRedirect(reverse(viewName, kwargs=kwargs, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)))   
    redirectView = staticmethod(redirectView)    
    
    # *****************************************************
    # This is a mature version of redirectView. However it hasn't implemented some of the old citizenHistory stuff 
    # or the famous menu_navF facebook quirk. Re-implement as needed.
    # It has a debug check to enforce redirect reasons which have gotten out of control
    def redirectTo(request, viewName, kwargs, reason, viewHistoryIndex=''):
        
        # viewHistoryIndex has priority, if supplied that's where the redirect goes
        redirectToView = True
        if viewHistoryIndex <> '':
            # But only if viewHistory has an entry for that index
            viewHistory = request.session.get('viewHistory', [request.META['PATH_INFO']])
            if len(viewHistory) > viewHistoryIndex: 
                redirectToView = False

        if redirectToView:
            return HttpResponseRedirect(reverse(viewName, kwargs=kwargs, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)))   
        else:
            return HttpResponseRedirect(viewHistory[viewHistoryIndex])   

    redirectTo = staticmethod(redirectTo)    
        
    # *****************************************************
    def auto_addEdit(request, formClass, fn_dict, object_id=None, toFormDict={}, successRedirectUrlName='', redirectKwargs={}):
        
        if object_id:
            redirectReason = 'edit'         
            form_action = request.META['duo_FormActionPrepend'] + reverse(request.META['auto_currentApp']+'_VIEW_Edit', kwargs = {'object_id':object_id}, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) 
            try:
                workObj = registeredClassInfo.get_classObject_fromBaseName(request.META['auto_currentApp_baseName']).objects.get(pk=object_id)
                resultDict = a_base_02.processForm_01(request, formClass, workObj, request.META['auto_currentApp']+'/templates/FORM_AddEdit.html',     resetFormOnSuccess=True,               toFormDict=toFormDict, form_action=form_action)
            except  ObjectDoesNotExist:
                raise Http404
        else:
            redirectReason = 'add'         
            form_action = request.META['duo_FormActionPrepend'] + reverse(request.META['auto_currentApp']+'_VIEW_Add', urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))
            resultDict = a_base_02.processForm_01(request, formClass, None,    request.META['auto_currentApp']+'/templates/FORM_AddEdit.html',     resetFormOnSuccess=True,               toFormDict=toFormDict, form_action=form_action)
        
        if resultDict['success']:
            i = resultDict['formInstance'].save(commit=False) 
            
            # dispatch the instance i and other parameters to the success function for further processing
            # it is the responsibility of the success function to save the instance to the database
            fn_dict['success'](i, request, resultDict['cleanData'], redirectReason)
            
            if successRedirectUrlName:
                return a_base_02.redirectView(request, successRedirectUrlName, redirectReason, redirectKwargs)
            else: 
                return a_base_02.redirectView(request, request.META['auto_currentApp']+'_VIEW_List', redirectReason, redirectKwargs)
        else: 
            contextDict = {}
            contextDict['vTitle'] = ''.join([redirectReason, " ", request.META['auto_currentApp_baseName']])    
            contextDict['main_1'] = resultDict['out']    
            return a_base_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')   
    auto_addEdit = staticmethod(auto_addEdit)
    
    # *****************************************************
    def auto_block_form(request, formClass, fn_dict, templateName, toFormDict={}, contextDict=None):
        form_action = request.META['duo_FormActionPrepend'] + request.META['PATH_INFO']
        resultDict = a_base_02.processForm_01(request, formClass, None, templateName, resetFormOnSuccess=True, toFormDict=toFormDict, form_action=form_action, contextDict=contextDict)
        
        if resultDict['success']:
            i = resultDict['formInstance'].save(commit=False) 
            
            # dispatch the instance i and other parameters to the success function for futher processing
            # it is the responsibility of the success function to save the instance to the database
            fn_dict['success'](i, request, resultDict['cleanData'], '')
        
            return {'success':0, 'out': resultDict['out']}
        else:
            return {'success':0, 'out': resultDict['out']}
    auto_block_form = staticmethod(auto_block_form)
            
    # *****************************************************
    def auto_form(request, formClass, fn_dict, viewName, templateName, viewName_kwargs={}, workObj=None, toFormDict={}, redirectOnSuccess=False, resetFormOnSuccess=True, contextDict=None):
        form_action = request.META['duo_FormActionPrepend'] + reverse(viewName, kwargs=viewName_kwargs, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))
        resultDict = a_base_02.processForm_01(request, formClass, workObj, templateName, resetFormOnSuccess=resetFormOnSuccess, toFormDict=toFormDict, form_action=form_action, contextDict=contextDict)
        
        if resultDict['success']:
            print resultDict
            i = resultDict['formInstance'].save(commit=False) 
            
            # dispatch the instance i and other parameters to the success function for futher processing
            # it is the responsibility of the success function to save the instance to the database
            fn_dict['success'](i, request, resultDict['cleanData'], '')
        
            if redirectOnSuccess: return {'success':1, 'out': ''}
            else:                 return {'success':0, 'out': resultDict['out']}
        else:
            return {'success':0, 'out': resultDict['out']}
    auto_form = staticmethod(auto_form)
    
    # *****************************************************
    # toFormDict: Will pass various things to the formClass init method. 
    #             That method MUST remove the various things from kwargs before calling super init otherwise 'unexpected keyword argument' will occur.
    #             See "class Form_app_boycottJoined_01(ModelForm)" for an example of how to do and use this.
    def processForm_01(request, formClass, workObj, templateName, contextDict=None,  resetFormOnSuccess=True, mode='block', toFormDict={}, form_action=''):
        context  = RequestContext(request)
        template = loader.get_template(templateName)
        prefix   = formClass.__name__
        
        resultDict = {'success':0, 'out':'', 'cleanData':''}    
        if contextDict is None: 
            contextDict = {}
            
        kwargs = toFormDict
        kwargs['prefix']   = prefix
        kwargs['instance'] = workObj
        if 'request' in kwargs:                   kwargs['request'] = request
        if 'hiddenUniqueIdentifier' in kwargs:    kwargs['prefix'] += "_%s" % (kwargs['hiddenUniqueIdentifier'])
            
        contextDict.update({'form_field_errors': ''})
        contextDict.update({'form_non_field_errors': ''})
        
        if request.method != 'POST': 
            formObj = formClass(**kwargs)
        else: 
            kwargs['data'] = request.POST
            formObj = formClass(**kwargs)
            
            if formObj.is_multipart():          
                formObj.files = request.FILES
            
            thisFormWasSubmitted = False
            for name in formObj.fields:
                if kwargs['prefix']+"-"+name in request.POST:
                    thisFormWasSubmitted = True
                    break
                
            if not thisFormWasSubmitted:
                del kwargs['data']
                formObj = formClass(**kwargs)
            else:
                try:
                    setInstanceWithExtraRequiredFormValidationValues = getattr(formObj, 'setInstanceWithExtraRequiredFormValidationValues')
                    setInstanceWithExtraRequiredFormValidationValues(request)
                except AttributeError, e:
                    pass       
                    
                if formObj.is_valid():
                    resultDict['cleanData']       = formObj.cleaned_data
                    resultDict['formInstance']    = formObj
                    resultDict['success']         = 1
                else:
                    contextDict.update({'form_field_errors': formObj.errors})
                      
#                    contextDict.update({'form_non_field_errors': formObj.non_field_errors().as_text()})
                    contextDict.update({'form_non_field_errors': formObj.non_field_errors()})


        # Check to see if the form has fields, if not return blank for resultDict['out']
        if len(formObj.fields):  
            if resultDict['success'] and resetFormOnSuccess: 
                del kwargs['instance']
                del kwargs['data']
                contextDict.update({'form': formClass(**kwargs)})
            else:      
                contextDict.update({'form': formObj})    
                
            if form_action: contextDict.update({'form_action': ' action="'+form_action+'"'})
            else:           print "*** %s form does NOT HAVE a form_action set" % (formClass)
                
            contextDict.update({'form_name': kwargs['prefix']})
            contextDict.update({'request': request})
                
            for key, value in contextDict.items():
                if callable(value): context[key] = value()
                else:               context[key] = value    
    
            if mode == 'block': resultDict['out'] =  template.render(context)
            else:               resultDict['out'] =  HttpResponse(template.render(context), mimetype=None)
        else: 
            resultDict['out'] = ''
        
        return resultDict
    processForm_01 = staticmethod(processForm_01)























            
    # *****************************************************
    def build_form_action(request, action_view, action_kwargs):
        return ''.join([request.META['duo_FormActionPrepend'], reverse(action_view, kwargs=action_kwargs, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))])
    build_form_action = staticmethod(build_form_action)
            
    # *****************************************************
    def get_result_dict(request, form_action, form_class, form_object, form_template, form_context_dict, form_build_dict, resetFormOnSuccess=True):
        context  = RequestContext(request)
        template = loader.get_template(form_template)
        prefix   = form_class.__name__
        
        resultDict = {'success':0, 'out':'', 'cleanData':''}    
            
        kwargs = form_build_dict
        kwargs['prefix']   = prefix
        kwargs['instance'] = form_object
        if 'request' in kwargs:                   kwargs['request'] = request
        if 'hiddenUniqueIdentifier' in kwargs:    kwargs['prefix'] += "_%s" % (kwargs['hiddenUniqueIdentifier'])
            
        form_context_dict.update({'form_field_errors': ''})
        form_context_dict.update({'form_non_field_errors': ''})
        
        if request.method != 'POST': 
            formObj = form_class(**kwargs)
        else: 
            kwargs['data'] = request.POST
            formObj = form_class(**kwargs)
            
            if formObj.is_multipart():          
                formObj.files = request.FILES
            
            thisFormWasSubmitted = False
            for name in formObj.fields:
                if kwargs['prefix']+"-"+name in request.POST:
                    thisFormWasSubmitted = True
                    break
                
            if not thisFormWasSubmitted:
                del kwargs['data']
                formObj = form_class(**kwargs)
            else:
                try:
                    setInstanceWithExtraRequiredFormValidationValues = getattr(formObj, 'setInstanceWithExtraRequiredFormValidationValues')
                    setInstanceWithExtraRequiredFormValidationValues(request)
                except AttributeError, e:
                    pass       
                    
                if formObj.is_valid():
                    resultDict['cleanData']       = formObj.cleaned_data
                    resultDict['formInstance']    = formObj
                    resultDict['success']         = 1
                else:
                    form_context_dict.update({'form_field_errors': formObj.errors})
                    form_context_dict.update({'form_non_field_errors': formObj.non_field_errors()})           #                    form_context_dict.update({'form_non_field_errors': formObj.non_field_errors().as_text()})

        # Check to see if the form has fields, if not return blank for resultDict['out']
        if len(formObj.fields):  
            if resultDict['success'] and resetFormOnSuccess: 
                del kwargs['instance']
                del kwargs['data']
                form_context_dict.update({'form': form_class(**kwargs)})
            else:      
                form_context_dict.update({'form': formObj})    
                
            form_context_dict.update({'form_action'   : ' action="'+form_action+'"'})
            form_context_dict.update({'form_name'     : kwargs['prefix']})
            form_context_dict.update({'request'       : request})
                
            for key, value in form_context_dict.items():
                if callable(value): context[key] = value()
                else:               context[key] = value    
    
            resultDict['out'] =  template.render(context)
        else: 
            resultDict['out'] = ''
        
        return resultDict
    get_result_dict = staticmethod(get_result_dict)

    
    