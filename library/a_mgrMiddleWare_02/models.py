# *********************************************************
# a_mgrMiddleWare_02/models.py

# *********************************************************
from a_base_02.models import a_base_02
from a_mgrApplication_03.models_aux import registeredClassInfo
import settings

mwMethods = {
                'request'       : [[1, 'a_base','mw_request_applicationInitialization_calledOnce']],       # by default we start off with a_base installed
                'view'          : [], 
                'response'      : [],
            }

# *********************************************************
class a_mgrMiddleWare_02(object):
    pass

    # -----------------------------------------------------
    def register_middlewareMethods(mw_methods_list, className):
        for x in mw_methods_list:
            a_mgrMiddleWare_02.mwAddMethod(x[0], x[1], className, x[2])
##            print "*** %-12s: x[0] = %3s, x[1] = %-20s, x[2] = %-40s" % ('register', x[0], x[1], x[2]) 
    register_middlewareMethods = staticmethod(register_middlewareMethods)         

    # -----------------------------------------------------
    def mwAddMethod(index, mode, className, method):
        if mode in mwMethods:
            if [index, className, method] not in mwMethods[mode]:    
                mwMethods[mode].append([index, className, method])
                mwMethods[mode].sort()      # hack to sort the items by index. I didn't bother to find a better place to put this as this only happens at __new__
            else:                                             print "*** mwAddMethod: className %s already in mwMethods[%s]" % (className, mode)
        else:                                                 print "*** mwAddMethod: mode %s NOT in mwMethods" % (mode)
    mwAddMethod = staticmethod(mwAddMethod) 

    # -----------------------------------------------------
    def mwDelMethod(index, mode, className, method):
        if mode in mwMethods:
            if [index, className, method] not in mwMethods[mode]:    print "*** mwDelMethod: className %s is NOT in mwMethods[%s]" % (className, mode)
            else:                                             mwMethods[mode].remove([index, className, method])
        else:                                                 print "*** mwDelMethod: mode %s NOT in mwMethods" % (mode)
    mwDelMethod = staticmethod(mwDelMethod) 
    
    # -----------------------------------------------------
    def continueForViewOnly(self, request, mode):
        if request.META['PATH_INFO'][:len(settings.MEDIA_PRJ)+1] <> ''.join(['/',settings.MEDIA_PRJ]) and request.META['PATH_INFO'][:len(settings.MEDIA_LIB)+1] <> ''.join(['/',settings.MEDIA_LIB]) and request.META['PATH_INFO'][:12] <> "/favicon.ico":
            return True
        else:                                                                                                           
            return False    

    # -----------------------------------------------------
    def process_request(self, request):
        rv = None
        if self.continueForViewOnly(request, 'request'):
            for x in mwMethods['request']:
##                print "*** %-12s: x[0] = %3s, x[1] = %-20s, x[2] = %-40s" % ('REQUEST', x[0], x[1], x[2]) 
                methodToCall = getattr(registeredClassInfo.get_classObject_fromBaseName(x[1]), x[2])
                rv = methodToCall(request)
                if rv is not None: break
        return rv
    
    # -----------------------------------------------------
    def process_view(self, request, view_func, view_args, view_kwargs):
        rv = None
        if self.continueForViewOnly(request, 'view'):
            for x in mwMethods['view']:
##                print "*** %-12s: x[0] = %3s, x[1] = %-20s, x[2] = %-40s" % ('VIEW', x[0], x[1], x[2]) 
                methodToCall = getattr(registeredClassInfo.get_classObject_fromBaseName(x[1]), x[2])
                rv = methodToCall(request, view_func, view_args, view_kwargs)                
                if rv is not None: break
        return rv      
    
    # -----------------------------------------------------
    def process_response(self, request, response):
        if self.continueForViewOnly(request, 'response'):
            for x in mwMethods['response']:
##                print "*** %-12s: x[0] = %3s, x[1] = %-20s, x[2] = %-40s" % ('RESPONSE', x[0], x[1], x[2]) 
                methodToCall = getattr(registeredClassInfo.get_classObject_fromBaseName(x[1]), x[2])
                response = methodToCall(request, response)              
        return response  