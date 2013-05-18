# *********************************************************
# e_thread_03/views.py

# *********************************************************
from a_mgrApplication_03.models_aux import registeredClassInfo
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from e_thread_03.models import e_thread_03, Form_e_thread_03, e_thread_replyTracking_03 
import simplejson

# *********************************************************
def e_thread_03_VIEW_List(request):
    QS  = e_thread_replyTracking_03.objects.filter(toCitizen=request.META['duo_citizen']).order_by('-auto_createdTimeStamp')
    display = e_thread_03.auto_list(request, QS, vTitle="Replies to your comments")
    
    # update the read boolean value for all unread items. Need to do this after the display output was captured above otherwise the display uses the new updated values.
    QS2 = QS.filter(read=False)
    QS2.update(read=True)
    
    return display  

# *********************************************************
def e_thread_03_VIEW_Detail(request, object_id):  
    return e_thread_03.auto_detail(request, object_id)

# *********************************************************
def e_thread_03_VIEW_Thread(request, instance, indent, mode):
    returnList      = []
    indentIncrement = 1
    
    QS = e_thread_03.objects.filter(auto_object_id__exact=instance.id,auto_content_type__exact=ContentType.objects.get_for_model(instance)).order_by('auto_createdTimeStamp')
    count = QS.count()
    
    # ---------------------------------------------------------
    if mode == 'link' or mode == 'min_link':
        if count == 0:      
            if request.META['duo_citizen'] is not None: 
                if request.META['duo_citizen'].authenticated == 1:  linkText = "add comment"
                else:                                               linkText = "no comments"
            else:                                                   linkText = "no comments"
        elif count == 1:                                            linkText = "1 comment"
        elif count > 1:                                             linkText = "%s comments" % (count)
        
        if linkText:
            if mode == 'link' or (mode == 'min_link' and count > 0):
                detailedViewName = "%s_VIEW_Detail" % (instance.__class__.__name__)                  
                
                if hasattr(instance, 'getUrl_detail'):   
                    link = instance.getUrl_detail(request, linkText)
                else:                               
                    link = "<a href='%s'>%s</a>" % (reverse(detailedViewName, kwargs = {'object_id':instance.id},       urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , linkText)
                returnList.append(link)
        
    # ---------------------------------------------------------
    elif mode == 'context':
        parentClassInstance = registeredClassInfo.get_classObject_fromContentTypeId(instance.auto_content_type_id)
        parentInstance      = parentClassInstance.objects.get(id=instance.auto_object_id)
        detailedViewName = "%s_VIEW_Detail" % (parentInstance.__class__.__name__)
        
        if hasattr(parentInstance, 'getUrl_detail'):   
            link = parentInstance.getUrl_detail(request, "context")            
        else:                                     
            link = "<a href='%s'>%s</a>" % (reverse(detailedViewName, kwargs = {'object_id':parentInstance.id},       urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , "context")
        returnList.append(link)
        
    # ---------------------------------------------------------
    elif mode == 'parent':
        parentClassInstance = registeredClassInfo.get_classObject_fromContentTypeId(instance.auto_content_type_id)
        parentInstance      = parentClassInstance.objects.get(id=instance.auto_object_id)        
        link = "<a href='#%s'>%s</a>" % (parentInstance.id,"parent")
        returnList.append(link)
        
    # ---------------------------------------------------------
    elif mode == 'unseen_permalink_parent':
        parentClassInstance         = registeredClassInfo.get_classObject_fromContentTypeId(instance.auto_content_type_id)
        parentInstance              = parentClassInstance.objects.get(id=instance.auto_object_id) 

        if instance.__class__.__name__ == 'e_thread_03':
            detailedViewName = "%s_VIEW_Detail" % (parentInstance.__class__.__name__)
            
            if hasattr(parentInstance, 'getUrl_detail'):   
                link = parentInstance.getUrl_detail(request, "parent")                 
            else:                                     
                link = "<a href='%s'>%s</a>" % (reverse(detailedViewName, kwargs = {'object_id':parentInstance.id},       urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , "parent")
            returnList.append(link)
        
    # ---------------------------------------------------------
    elif mode == 'permalink':
        detailedViewName    = "%s_VIEW_Detail" % (instance.__class__.__name__)
        
        if hasattr(instance, 'getUrl_detail'):   
            link = instance.getUrl_detail(request, "permalink")               
        else:                               
            link = "<a href='%s'>%s</a>" % (reverse(detailedViewName, kwargs = {'object_id':instance.id},        urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , "permalink")
        returnList.append(link)
        
    # ---------------------------------------------------------
    elif mode == 'indentedchildren':
        detailedViewName    = "%s_VIEW_Detail" % (instance.__class__.__name__)
        if hasattr(instance, 'getUrl_detail'):   
            link = instance.getUrl_detail(request, "more replies")               
        else:                               
            link = "<a href='%s'>%s</a>" % (reverse(detailedViewName, kwargs = {'object_id':instance.id},       urlconf=getattr(request, "urlconf", settings.ROOT_URLCONF)) , "more replies")
        returnList.append(link)

    # ---------------------------------------------------------
    elif mode == 'start':
        if request.META['duo_citizen'] is not None: 
            if request.META['duo_citizen'].authenticated == 1:   
                returnList.append(e_thread_03_VIEW_Thread(request, instance, indent, mode="internal_form"))
            else:                                               
                returnList.append("<br><span class='mmh-replyErrorText'>Your account has to be authenticated before you can comment.</span>")
        else:
            returnList.append('<br><span class="mmh-replyErrorText">You must be signed in to comment.</span>')

        for x in QS:
            returnList.append(e_thread_03_VIEW_Thread(request, x, indent, mode="entry"))

    # ---------------------------------------------------------
    elif mode == 'entry':
        
        max_indent = 8
        
        returnList.append(e_thread_03.processTemplate_01(request, 'e_thread_03/templates/BLOCK_Entry.html', {'object':instance,'indent':indent,'remainder':14-indent,'max_indent':max_indent}))
        new_indent = indent + indentIncrement
        
        if indent < max_indent:
            for x in QS:
                returnList.append(e_thread_03_VIEW_Thread(request, x, new_indent, mode="entry"))
            
    # ---------------------------------------------------------
    elif mode == 'internal_form':
        returnList.append(e_thread_03_FORM_ThreadEntry(request, instance, indent, 14-indent))

    # ---------------------------------------------------------
    else:
        returnList.append("Error: unknown mode (%s)" % (mode))
     
    return ''.join(returnList)
        
# *********************************************************
def e_thread_03_FORM_ThreadEntry(request, instance, indent, remainder):
    contextDict = {}    
    
    # Since a thread instance can hang from any class I need to record both the 
    # content_type_id and instance id for the object getting this thread item. 
    # I'm passing both in hiddenUniqueIdentifier as a string which can be split
    # by the token ":". 
    # An example: "18:2" which this is being hung from an e comment 03 
    # contentype (18) and instance id = 2 
    
    auto_content_type_id = ContentType.objects.get_for_model(instance).id
    hiddenId = "%s:%s" % (auto_content_type_id, instance.id)

    fn_dict = {'success' : FORM_ThreadEntry_processSuccess}
    rDict = e_thread_03.auto_block_form(
                                             request, 
                                             Form_e_thread_03, 
                                             fn_dict, 
                                             'e_thread_03/templates/FORM_ThreadEntry.html', 
                                             toFormDict={'hiddenUniqueIdentifier':hiddenId},      
                                             contextDict={"indent":indent,"remainder":remainder},                                      
                                       )
    return rDict['out']

# *********************************************************
def FORM_ThreadEntry_processSuccess(*args):
    
    # args[0] = i (the instance)
    # args[1] = request
    # args[2] = cleanDataDict
    # args[3] = redirectReason ('edit' or 'add')
    
#    print "+++ args[0] = %s" % (args[0])
#    print "+++ args[1] = %s" % (args[1])
#    print "+++ args[2] = %s" % (args[2])
#    print "+++ args[3] = %s" % (args[3])

    parts = args[2]['hiddenUniqueIdentifier'].split(':', 1)

    # Use the value of the hidden variable hiddenWasEdited to determine if this is an edit of an existing item or an insert of a new one
    if args[2]['hiddenWasEdited'] == "1":
        try:
            instance = e_thread_03.objects.get(pk=parts[1])
            instance.comment = args[2]['comment']
            instance.edited  = True
            instance.save(request=args[1])
        except ObjectDoesNotExist:
            print "*** FORM_ThreadEntry_processSuccess: error the e_thread_03 item (id = %s) I'm trying to edit doesn't exist." % (parts[1])
    else:
        args[0].comment                 = args[2]['comment'].strip()
        args[0].auto_content_type_id    = parts[0]
        args[0].auto_object_id          = parts[1]
        args[0].save(request=args[1])
   
        parentClassInstance = registeredClassInfo.get_classObject_fromContentTypeId(parts[0])
        parentInstance      = parentClassInstance.objects.get(id=parts[1])
        
        # Add a reply tracking instance
        replyTrackingInstance = e_thread_replyTracking_03()
        replyTrackingInstance.post          = args[0]
        replyTrackingInstance.toCitizen     = parentInstance.auto_citizen
        replyTrackingInstance.save(request=args[1])
        

# *********************************************************
def e_thread_03_VIEW_Raw(request, object_id):  
    try:
        obj2detail = e_thread_03.objectsAll.get(pk=object_id)
#        print "obj2detail.comment = %s" % (obj2detail.comment)
        return HttpResponse(obj2detail.comment, mimetype='application/javascript')    
    except  ObjectDoesNotExist:
        raise Http404   

# *********************************************************
def e_thread_03_VIEW_BBcode(request, object_id):  
    try:
        obj2detail = e_thread_03.objectsAll.get(pk=object_id)
        return e_thread_03.processTemplate_01(request, 'e_thread_03/templates/BLOCK_BBcode.html', {'object': obj2detail}, mode='view')
    except  ObjectDoesNotExist:
        raise Http404   
    
