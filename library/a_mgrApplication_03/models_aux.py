# *********************************************************
# a_mgrApplication_03/models_aux.py

from django.contrib.contenttypes.models import ContentType

# *********************************************************
internalRegisteredClassesDict        = {}

class registeredClassInfo(object):
    classObject                     = None
    entryInit_class                 = True
    entryInit_middlewareMethods     = True
    entryInit_c_nav_02_menu         = True
    entryInit_dependencies          = True
    entryInit_sideBarMethods        = True
    
    # -----------------------------------------------------
    def add_newEntry(baseName, classObject):
        if baseName not in internalRegisteredClassesDict:
            internalRegisteredClassesDict[baseName] = registeredClassInfo()
            internalRegisteredClassesDict[baseName].classObject = classObject
    add_newEntry = staticmethod(add_newEntry)   
    
    # -----------------------------------------------------
    def get_classObject_fromBaseName(baseName):
        return internalRegisteredClassesDict[baseName].classObject
    get_classObject_fromBaseName = staticmethod(get_classObject_fromBaseName)   
    
    # -----------------------------------------------------
    def get_classObject_fromContentTypeId(id):
        contentTypeInstance = ContentType.objects.get(pk=id)
        return contentTypeInstance.model_class()
    get_classObject_fromContentTypeId = staticmethod(get_classObject_fromContentTypeId)   
    
    # -----------------------------------------------------
    def set_entryUnused(baseName, entryName):
        internalRegisteredClassesDict[baseName].entryName = False    
    set_entryUnused = staticmethod(set_entryUnused)      
    
    # -----------------------------------------------------
    def get_items():
        return internalRegisteredClassesDict.items()
    get_items = staticmethod(get_items) 
    
    # -----------------------------------------------------
    def clear_internalRegisteredClassesDict():
        internalRegisteredClassesDict = {}
    clear_internalRegisteredClassesDict = staticmethod(clear_internalRegisteredClassesDict) 