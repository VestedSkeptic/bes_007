# *********************************************************
# d_move_02/views.py
# *********************************************************

from d_move_02.models import d_move_02, Form_d_move_02
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
from httplib import HTTPException
from os.path import join, exists
import os
import settings
import tempfile
import time

# *********************************************************
def d_move_02_VIEW_home(request):
    d_move_02.setTitle(request, "Move")
    contextDict = {}
    
    QS = d_move_02.objects.order_by('date_timestamp')
    
    contextDict['main_1'] = d_move_02.processTemplate_01(request, 'd_move_02/templates/B_home.html', {
                                                                                                      'laps':QS,
                                                                                                    })    

    return d_move_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')   




# *********************************************************
def d_move_02_VIEW_addLap(request):
    contextDict = {}

    fn_dict = {'success' : Withdrawal_processSuccess}
    rDict1 = d_move_02.auto_form(
                                      request, 
                                      Form_d_move_02, 
                                      fn_dict, 
                                      'd_move_02_VIEW_addLap', 
                                      'd_move_02/templates/FORM_AddLap.html',
                                      redirectOnSuccess=True,
                                      )
    if rDict1['success']:
        return d_move_02.redirectView(request, "d_move_02_VIEW_home", 'deleteU') 
    else:
        contextDict['main_1']                       = rDict1['out']
        return d_move_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')

# *********************************************************
def Withdrawal_processSuccess(*args):
    # args[0] = i (the instance)
    # args[1] = request
    # args[2] = cleanDataDict
    # args[3] = redirectReason ('edit' or 'add')
    
    args[0].date_timestamp = time.mktime(time.strptime(args[0].date, "%Y-%m-%d"))
    args[0].save(request=args[1])