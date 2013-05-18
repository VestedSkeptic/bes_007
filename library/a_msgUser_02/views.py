# *********************************************************
# a_msgUser_02/views.py

# *********************************************************
from a_msgUser_02.models import a_msgUser_02, a_msgUser_global_02, Form_a_msgUser_global_02 

# *********************************************************
def a_msgUser_02_VIEW_Detail(request, object_id):     
    return a_msgUser_02.auto_detail(request, object_id)

# *********************************************************
def a_msgUser_02_VIEW_Delete(request, object_id, confirm=''):
    return a_msgUser_02.auto_delete(request, object_id, confirm)

# *********************************************************
def a_msgUser_02_VIEW_List(request):
    QS = a_msgUser_02.objects.filter(toCitizen__exact=request.META['duo_citizen']).order_by('read', '-auto_timeStamp', 'title')
    return a_msgUser_02.auto_list(request, QS, vTitle = 'System Messages')

# *********************************************************
def a_msgUser_02_VIEW_ToggleRead(request, object_id):
    instance = a_msgUser_02.objects.get(pk=object_id)
    
    if instance.toCitizen == request.META['duo_citizen']:
        if instance.read: instance.read = False
        else:             instance.read = True
        instance.save(request=request)

    return a_msgUser_02.redirectView(request, 'a_msgUser_02_VIEW_List', 'readToggle', {})

# *********************************************************
def a_msgUser_global_02_VIEW_Detail(request, object_id):  
    contextDict = {}
    obj2detail = a_msgUser_global_02.objectsAll.get(pk=object_id)
    contextDict['main_1'] = a_msgUser_global_02.processTemplate_01(request, 'a_msgUser_02/templates/B_detail.html', {'object': obj2detail})
    return a_msgUser_global_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view') 

# *********************************************************
def a_msgUser_global_02_VIEW_Delete(request, object_id, confirm=''):
    return a_msgUser_global_02.auto_delete_02(request, object_id, confirm, vTitle='Delete Global Message', template='B_detail')      

# *********************************************************
def a_msgUser_global_02_VIEW_List(request):
    contextDict = {}
    contextDict['vTitle'] = 'Global Messages'
    
    QS1 = a_msgUser_global_02.objects.order_by('-auto_createdTimeStamp')
    
    contextDict['main_1']   = a_msgUser_global_02.processTemplate_02_withPagination(request, 'a_msgUser_02/templates/B_list.html', {'objectList': QS1}, contextPaginationKey='objectList')    
    return a_msgUser_global_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')

# *********************************************************
def a_msgUser_global_02_VIEW_Add(request):
    contextDict         = {'vTitle':'Add Global Message'}    
    action_view         = 'a_msgUser_global_02_VIEW_Add'
    action_kwargs       = {}
    form_action         = a_msgUser_global_02.build_form_action(request, action_view, action_kwargs)
    
    form_class          = Form_a_msgUser_global_02
    form_object         = None
    form_template       = 'a_msgUser_02/templates/F_addEdit.html'
    form_title          = contextDict['vTitle']
    form_context_dict   = {'form_title':form_title}
    form_build_dict     = {}
    result_dict         = a_msgUser_global_02.get_result_dict(request, form_action, form_class, form_object, form_template, form_context_dict, form_build_dict, resetFormOnSuccess=True)    
    
    if result_dict['success']:
        instance = result_dict['formInstance'].save(commit=False) 

        # -----------------------------------------------------
        # process form results
        # conversion: args[0] = instance, args[1] = request, args[2] = result_dict['cleanData'], args[3] = redirectReason  
        
        instance.save(request=request)
        
        # -----------------------------------------------------
        contextDict = {'vTitle':'Global Message Added'}    
        contextDict['main_1'] = instance.render_detail(request)
        return a_msgUser_global_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')
    else:
        contextDict['main_1'] = result_dict['out']
        return a_msgUser_global_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')    

# *********************************************************
def a_msgUser_global_02_VIEW_Edit(request, object_id):
    contextDict         = {'vTitle':'Edit Global Message'}    
    action_view         = 'a_msgUser_global_02_VIEW_Edit'
    action_kwargs       = {'object_id':object_id}
    form_action         = a_msgUser_global_02.build_form_action(request, action_view, action_kwargs)
    
    form_class          = Form_a_msgUser_global_02
    form_object         = a_msgUser_global_02.objects.get(pk=object_id)
    form_template       = 'a_msgUser_02/templates/F_addEdit.html'
    form_title          = contextDict['vTitle']
    form_context_dict   = {'form_title':form_title}
    form_build_dict     = {}
    result_dict         = a_msgUser_global_02.get_result_dict(request, form_action, form_class, form_object, form_template, form_context_dict, form_build_dict, resetFormOnSuccess=True)    
    
    if result_dict['success']:
        instance = result_dict['formInstance'].save(commit=False) 

        # -----------------------------------------------------
        # process form results
        # conversion: args[0] = instance, args[1] = request, args[2] = result_dict['cleanData'], args[3] = redirectReason  
        
        instance.save(request=request)
        
        # -----------------------------------------------------
        contextDict = {'vTitle':'Global Message Edited'}    
        contextDict['main_1'] = instance.render_detail(request)
        return a_msgUser_global_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')
    else:
        contextDict['main_1'] = result_dict['out']
        return a_msgUser_global_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view') 
