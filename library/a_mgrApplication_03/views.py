# *********************************************************
# a_mgrApplication_03/views.py

# *********************************************************
from a_mgrApplication_03.models import a_mgrApplication_03, Form_a_mgrApplication_03, subscription_01, genericUserAppSubscription, genericUserAppVote
from a_base_02.models import secDict
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

# *********************************************************
def a_mgrApplication_03_newCitizenDefaultSubscriptions(request):
    apps = a_mgrApplication_03.objects.all()
    for app in apps:
        newSubscription = subscription_01()
        newSubscription.application = app
        newSubscription.save(request=request)

# *********************************************************
def a_mgrApplication_03_VIEW_Delete(request, object_id, confirm=''):
#    return a_mgrApplication_03.auto_delete(request, object_id, confirm)   
    return a_mgrApplication_03.auto_delete_02(request, object_id, confirm, template='BLOCK_Detail')   

# *********************************************************
def a_mgrApplication_03_VIEW_Add(request):
    fn_dict = {'success' : AddEdit_processSuccess}
    return a_mgrApplication_03.auto_addEdit(request, Form_a_mgrApplication_03, fn_dict, None, toFormDict={})

# *********************************************************
def a_mgrApplication_03_VIEW_Edit(request, object_id):
    fn_dict = {'success' : AddEdit_processSuccess}
    instance = a_mgrApplication_03.objects.get(pk=object_id)
    return a_mgrApplication_03.auto_addEdit(request, Form_a_mgrApplication_03, fn_dict, object_id, toFormDict={}, successRedirectUrlName=a_mgrApplication_03_VIEW_List)

# *********************************************************
def AddEdit_processSuccess(*args):
    # args[0] = i (the instance)
    # args[1] = request
    # args[2] = cleanDataDict
    # args[3] = redirectReason ('edit' or 'add')
    
    args[0].save(request=args[1])

# *********************************************************
def a_mgrApplication_03_VIEW_subscribetoggle(request, object_id):
    instance = a_mgrApplication_03.objects.get(pk=object_id)
    QS = subscription_01.objects.filter(application=instance, auto_citizen__exact=request.META['duo_citizen'])

    if QS.count():
        QS[0].delete()
    else:
        newSubscription = subscription_01()
        newSubscription.application = instance
        newSubscription.save(request=request)
    
    return a_mgrApplication_03.redirectView(request, 'a_mgrApplication_03_VIEW_List', 'admFormPr')

# *********************************************************
def a_mgrApplication_03_VIEW_List(request):
    contextDict = {}    
    objectList  = []
    
    subList = []
    notList = []

    if (request.META['citizen_rights'] == secDict['s_developer']):
        QS = a_mgrApplication_03.objects.order_by('name')
    else:
        QS = a_mgrApplication_03.objects.exclude(released=False).order_by('name')
        
    for x in QS:
        QS2 = subscription_01.objects.filter(application=x, auto_citizen__exact=request.META['duo_citizen'])
        if QS2.count(): subList.append([x, 'unsubscribe'])
        else:           notList.append([x, 'subscribe'])    
        
    objectList = subList + notList 


    contextDict['main_1'] = a_mgrApplication_03.processTemplate_02_withPagination(request, 'a_mgrApplication_03/templates/BLOCK_List.html', contextDict={'objectList':objectList}, contextPaginationKey='objectList')
    return a_mgrApplication_03.processTemplate_01(request, 'BASE.html', contextDict, mode='view')

# *********************************************************
def a_mgrApplication_03_VIEW_Detail(request, object_id):  
    contextDict = {}
    obj2detail = a_mgrApplication_03.objectsAll.get(pk=object_id)
    QS2 = subscription_01.objects.filter(application=obj2detail, auto_citizen__exact=request.META['duo_citizen'])
    if QS2.count(): objectList = [obj2detail, 'unsubscribe']
    else:           objectList = [obj2detail, 'subscribe']   
    
    contextDict['vTitle'] = obj2detail
    contextDict['main_1'] = a_mgrApplication_03.processTemplate_01(request, 'a_mgrApplication_03/templates/BLOCK_Detail.html', contextDict={'object': objectList})
    return a_mgrApplication_03.processTemplate_01(request, 'BASE.html', contextDict, mode='view') 

# *********************************************************
def a_mgrApplication_03_VIEW_genericUserAppSubscriptionToggle(request):
    # Determine if there is a subscription
    contentTypeObj = ContentType.objects.get(name__exact=request.POST['content_type'])
    QS = genericUserAppSubscription.objects.filter(
                                                   auto_object_id__exact        = request.POST['object_id'],
                                                   auto_content_type__exact     = contentTypeObj,
                                                   auto_citizen__exact          = request.META['duo_citizen']
                                                   ) 

    if QS.count():
        QS.delete()
#        print "*** subscription deleteted"    
    else:
        newSubscription = genericUserAppSubscription()
        newSubscription.auto_content_object = contentTypeObj.model_class().objects.get(pk=request.POST['object_id'])
        newSubscription.save(request=request)    
#        print "*** subscription added"    

    # HACK: To ensure this view returns a request object
    contextDict = {}
    return a_mgrApplication_03.processTemplate_01(request, 'BASE.html', contextDict, mode='view') 

# *********************************************************
def a_mgrApplication_03_VIEW_genericUserAppVote(request, mode, vote):
#    print "*************************************************************"
#    print "*** a_mgrApplication_03_VIEW_genericUserAppVote"
#    print "request.POST = %s" % (request.POST)
#    print "request.POST['object_id'] = %s"    % (request.POST['object_id'])
#    print "request.POST['content_type'] = %s" % (request.POST['content_type'])
#    print "request.META['duo_citizen'] = %s"  % (request.META['duo_citizen'])

    # Get users current vote
    contentTypeObj = ContentType.objects.get(name__exact=request.POST['content_type'])
#    contentTypeObj = ContentType.objects.get(name__exact='p_problem_01')
    try:
        usersCurrentVote = genericUserAppVote.objects.get(
                                                       auto_object_id__exact        = request.POST['object_id'],
#                                                       auto_object_id__exact        = 1,
                                                       auto_content_type__exact     = contentTypeObj,
                                                       mode__exact                  = mode,
                                                       auto_citizen__exact          = request.META['duo_citizen'],
                                                       )
        
        if int(usersCurrentVote.vote) == int(vote):     # Delete existing vote if it equals the same vote because this means the citizen toggled it off
            usersCurrentVote.delete(request=request)
        else:                                           # save new vote for citizen 
            usersCurrentVote.vote = vote
            usersCurrentVote.save(request=request)    
    except ObjectDoesNotExist:
        usersCurrentVote = genericUserAppVote()
        usersCurrentVote.auto_content_object = contentTypeObj.model_class().objects.get(pk=request.POST['object_id'])
#        usersCurrentVote.auto_content_object = contentTypeObj.model_class().objects.get(pk=1)
        usersCurrentVote.mode                = mode
        usersCurrentVote.vote                = vote
        usersCurrentVote.save(request=request)    

    # HACK: To ensure this view returns a request object
    contextDict = {}
    return a_mgrApplication_03.processTemplate_01(request, 'BASE.html', contextDict, mode='view') 

