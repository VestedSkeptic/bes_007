# *********************************************************
# base_tag.py

# *********************************************************
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import RegexURLResolver
from django.template import Library, Node #, TextNode
from django.template import TemplateSyntaxError
from django.template import resolve_variable
from django.template.loader import get_template
from django.utils.text import truncate_words
from a_library_02 import engine_permissions
import settings
import time

from a_library_02.templatetags.bt_thread_03             import bt_thread_03
##from a_library_02.templatetags.bt_comment_03            import bt_comment_03
from a_library_02.templatetags.bt_citizen_03            import bt_citizen_03, bt_citizenLink_03, bt_autoCitizenLink_03
from a_library_02.templatetags.bt_time_03               import bt_time_03
from a_library_02.templatetags.bt_interface_03          import bt_interface_03_edit, bt_interface_03_delete
#from a_library_02.templatetags.bt_friend_03             import bt_friendRequestLink_03
from a_library_02.templatetags.bt_subscribe_03          import bt_subscribe_03
from a_library_02.templatetags.bt_vote_03               import bt_vote_03
from a_library_02.templatetags.bt_tags_03               import bt_tags_03
#from a_discussion_01.templatetags.bt_discussion_01      import bt_discussion_01

register = Library()

###    appURL                          name of a view                                              what to display                     optional object id
###    appURL_NoUnderline                                                                                                              requirement assumed by use
###    
###    
###{% appURL                           a_citizen_02_VIEW_Detail                                    object.id                          object.id                                                %}
###{% appURL                           a_citizen_02_VIEW_Detail                                    object.id                          object.id                                                %}
###{% appURL_NoUnderline               a_citizen_02_VIEW_Detail                                    request.META.duo_citizen.name      request.META.duo_citizen.id                              %}
###{% appURL_NoUnderline               a_citizen_02_VIEW_Logout                                    "log out"                                                                                   %}
###{% appURL                           a_urlPassChange_02_VIEW_changeRequest                       "Recover password"                                                                          %}
###{% appURL_NoUnderline               c_iurlRaw_02_VIEW_ListCategory                              x.1.name                            x.1.id                                                  %}
###{% appURL                           a_mgrCategories_02_VIEW_Edit                                "e"                                 x.1.id                                                  %}
###{% appURL                           a_update_02_VIEW_ResetTo                                    "reset to"                          objInfo.0.2                                             %}


##New Format
##                    app                    [obj]            [DisplayText]                
##{% base_tag         discussionThread       OBJECT=obj       DISPLAY=""            DISPLAY_PRE_IF=""         DISPLAY_POST_IF=""      APP_FLAGS=""  %}

pFlagsKnownList = ["resolve"]

# *********************************************************
@register.tag(name="baseTag")
def baseTag(parser, token):
    return baseTag_parseAndRender(parser, token)

# *********************************************************
def baseTag_parseAndRender(parser, token, noUnderline=False, urlIfTrunc=False):
    returnList  = []
    resolveDict = {}
    paramDict   = {}
    app         = ""
    
    bits = token.split_contents()
    
    if len(bits) < 2:
        app = "None"
        returnList.append("Only 1 bit passed in.")
    else:
        app = bits[1]
        
    if len(bits) > 2:
        for x in bits[2:]:
            k, v = x.split('=', 1)
           
            if k not in paramDict: 
                parts = v.split(':', 1)
                if len(parts) == 1:
                    paramDict[k] = v
                else:
                    paramDict[k] = parts[0]
                    
                    if parts[1] == 'resolve':
                        resolveDict[k] = parser.compile_filter(paramDict[k]) 
                    else:
                        returnList.append("Unknown part[1] (%s) passed in." % (parts[1]))
            else:                  
                returnList.append("Duplicate parameter %s with value %s detected." % (k, v))
            
    if      app == "bt_thread_03":                  return bt_thread_03                 (paramDict, returnList, resolveDict)
##    elif    app == "bt_comment_03":                 return bt_comment_03                (paramDict, returnList, resolveDict)
    elif    app == "bt_citizen_03":                 return bt_citizen_03                (paramDict, returnList, resolveDict)
    elif    app == "bt_citizenLink_03":             return bt_citizenLink_03            (paramDict, returnList, resolveDict)
    elif    app == "bt_autoCitizenLink_03":         return bt_autoCitizenLink_03        (paramDict, returnList, resolveDict)
    elif    app == "bt_time_03":                    return bt_time_03                   (paramDict, returnList, resolveDict)
    elif    app == "bt_time_03":                    return bt_time_03                   (paramDict, returnList, resolveDict)
    elif    app == "bt_interface_03_edit":          return bt_interface_03_edit         (paramDict, returnList, resolveDict)
    elif    app == "bt_interface_03_delete":        return bt_interface_03_delete       (paramDict, returnList, resolveDict)
    elif    app == "bt_friendRequestLink_03":       return bt_friendRequestLink_03      (paramDict, returnList, resolveDict)
    elif    app == "bt_subscribe_03":               return bt_subscribe_03              (paramDict, returnList, resolveDict)
    elif    app == "bt_vote_03":                    return bt_vote_03                   (paramDict, returnList, resolveDict)
    elif    app == "bt_tags_03":                    return bt_tags_03                   (paramDict, returnList, resolveDict)
    elif    app == "bt_discussion_01":              return bt_discussion_01             (paramDict, returnList, resolveDict)
