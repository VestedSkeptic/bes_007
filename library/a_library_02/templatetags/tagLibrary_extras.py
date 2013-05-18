from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import RegexURLResolver
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import Library, Node #, TextNode
from django.template import TemplateSyntaxError
from django.template import resolve_variable
from django.template.loader import get_template
from django.utils.text import truncate_words
from a_library_02 import engine_permissions
import settings
import time

register = Library()

trunkWordToken          = "more ..."

# *********************************************************
def getFunctionStringForNamedUrlPattern(namedUrlPattern):
    uResolve = RegexURLResolver(r'^/', 'urls_root')   
    rDict = uResolve.reverse_dict
    returnString = ''
    for key, value in rDict.items():
        if key == namedUrlPattern:
            for v in value:
                if not isinstance(v, RegexURLResolver):
                    print "*** v = %s" % (v)
#                    returnString = v.callback.__name__
                    break
                
    if namedUrlPattern <> returnString:
        print "*** ERROR: namedUrlPattern [%s] <> returnString [%s]" % (namedUrlPattern, returnString)
        
    return returnString

# *********************************************************
class appUrlNode(template.Node):   
    def __init__(self, view_name, dt_args, args, kwargs, oargs, displayTextNeedsResolving, noUnderline=False, urlTruncLength=0):
        self.view_name                   = view_name
        self.dt_args                     = dt_args
        self.displayTextNeedsResolving   = displayTextNeedsResolving
        self.args                        = args
        self.kwargs                      = kwargs
        self.oargs                       = oargs
        self.noUnderline                 = noUnderline
        self.urlTruncLength              = urlTruncLength
        
        # since I have a one to one relationship between my function names and my view names I should be able to 
#        if settings.DEBUG: self.funcString = getFunctionStringForNamedUrlPattern(self.view_name)
#        else:              self.funcString = self.view_name
        self.funcString = self.view_name
        
    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(k, v.resolve(context)) for k, v in self.kwargs.items()])
        
        if self.displayTextNeedsResolving: self.display_text = self.dt_args[0].resolve(context)
        else:                              self.display_text = self.dt_args[0]  

        reverse_out = ''
        returnLink = []
        
        if self.urlTruncLength:
            trunkWords = truncate_words(self.display_text, self.urlTruncLength)
            if trunkWords[-3:] <> "...":    # django's truncate_words auto appends "..." if truncate happened
                return self.display_text
            else:                                
                returnLink.append(trunkWords[:-3])
                returnLink.append(' ')
                self.display_text = trunkWordToken

        request = resolve_variable('request', context)  # Interesting way to get the request variable from the context
        
        for k in context:
            try:
                urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
                reverse_out = reverse(self.view_name, args=args, kwargs=kwargs, urlconf=urlconf)
            except NoReverseMatch:
                print "*** appUrlNode NoReverseMatch Error: self.view_name = %s, args = %s, kwargs = %s, urlconf = %s" % (self.view_name, args, kwargs, urlconf)
#                try:
#                    project_name = settings.SETTINGS_MODULE.split('.')[0]
#                    reverse_out = reverse(project_name + '.' + self.view_name, args=args, kwargs=kwargs, urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF))
#                except NoReverseMatch:
#                    pass
                        
        if len(reverse_out):
            # check users security permissions to see if they have access to the view this URL is pointing at
            if engine_permissions.checkUserPermissions(request.META['citizen_rights'], self.funcString, self.args, self.kwargs, request):

                noUnderlineStyle = ''
                if self.noUnderline:
                    noUnderlineStyle = 'STYLE="text-decoration:none"'
                    
                # prepending link with site FormActionPrepend for absolute links NOT relative ones
                if len(self.oargs): returnLink.append("%s<a %s href='%s%s'>%s</a>%s" % (self.oargs[0], noUnderlineStyle, resolve_variable('request.META.duo_FormActionPrepend', context), reverse_out, self.display_text, self.oargs[1]))
                else:               returnLink.append("<a %s href='%s%s'>%s</a>"     % (noUnderlineStyle, resolve_variable('request.META.duo_FormActionPrepend', context), reverse_out, self.display_text))
            else:
                if settings.DEBUG: returnLink.append("<strike>" + str(self.display_text) + "</strike>")   
                else:              returnLink.append('')  
        else:
            if settings.DEBUG: returnLink.append("<blink>[" + self.display_text + "]</blink>")   
        
        return ''.join(returnLink)
                
# *********************************************************
def appURLguts(parser, token, noUnderline=False, urlIfTrunc=False):
    bits = token.split_contents()
    
    if len(bits) < 3:
        raise TemplateSyntaxError, "'%s' takes at least two arguments (path to a view) (display text - in quotes?)" % bits[0]
    args   = []
    kwargs = {}
    oargs  = []
    
    if len(bits) > 3:
        for arg in bits[3].split(','):
            if '=' in arg:
                k, v = arg.split('=', 1)
                k = k.strip()
                if k == 'opt':
                    o1, o2 = v.split('!', 1)
                    oargs.append(o1)                   
                    oargs.append(o2)                   
                else:    
                    kwargs[k] = parser.compile_filter(v)
            else:
                args.append(parser.compile_filter(arg))
                
    dt_args = []
    display_text = bits[2]
    
    urlTruncLength = 0
    if urlIfTrunc: urlTruncLength = bits[4]
    
    # if quotes are around display text strip them
    if (display_text[0] == display_text[-1] and display_text[0] in ('"', "'")): 
        dt_args.append(display_text[1:-1])     
        displayTextNeedsResolving = False
    # otherwise this must be an element which must be resolved so....    
    else:
        dt_args.append(parser.compile_filter(display_text))     
        displayTextNeedsResolving = True 
    
    return appUrlNode(bits[1], dt_args, args, kwargs, oargs, displayTextNeedsResolving, noUnderline, urlTruncLength)    

# *********************************************************
@register.tag(name="appURL")
def do_appURL(parser, token):
    return appURLguts(parser, token)

# *********************************************************
@register.tag(name="appURL_NoUnderline")
def do_appURL_NoUnderline(parser, token):
    return appURLguts(parser, token, noUnderline=True)

# *********************************************************
@register.tag(name="moreTruncURL")
def do_appURL(parser, token):
    return appURLguts(parser, token, urlIfTrunc=True)

# *********************************************************
@register.filter
def default_if_length_zero(value, arg): 
    "returns arg if length of input value is zero"
    if len(value) == 0: return arg 
    else:               return value

# *********************************************************
@register.filter
def timestampFormat(value, arg): 
    "returns timestamp as formatted"
    return time.strftime(arg,time.localtime(value))

# *********************************************************
class ConstantIncludeNode(Node):
    def __init__(self, template_path, mode):
        self.mode = mode
        self.modeList = ['list','detail','banner_16','sticky_16','stky_ahvs','bann_ahvs']
        try:
            t = get_template(template_path)
            self.template = t
        except:
            if settings.TEMPLATE_DEBUG:
                raise
            self.template = None

    def render(self, context):
        if self.template:
            if self.mode not in self.modeList:
                print "*** Error: include_mode (%s) is not in modeList (%s)" % (self.mode, self.modeList)
            for x in self.modeList:
                if x == self.mode: context['include_mode_'+x] = True
                else:              context['include_mode_'+x] = False 
            return self.template.render(context)
        else:
            return ''

# *********************************************************
# A modified version of django's include filter which takes an extra
# mode parameter and passes this to the included template allowing that
# template to be rendered based on that mode parameter value
@register.tag(name="include_mode")
def _include_mode(parser, token):
    bits = token.contents.split()
    if len(bits) != 3:
        raise TemplateSyntaxError, "%r tag takes two arguments: the name of the template to be included and a mode parameter" % bits[0]
    path = bits[1]
    mode = bits[2]
#    if path[0] in ('"', "'") and path[-1] == path[0]:
#        return ConstantIncludeNode(path[1:-1])
#    return IncludeNode(bits[1])
    return ConstantIncludeNode(path[1:-1], mode[1:-1])