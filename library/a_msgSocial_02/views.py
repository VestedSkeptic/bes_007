# *********************************************************
# a_msgSocial_02/views.py

# *********************************************************
from a_msgSocial_02.models import a_msgSocial_02
#import simplejson
#from django.core.exceptions import ObjectDoesNotExist
#from a_citizen_02.models import a_citizen_02
#import settings

# *********************************************************
def a_msgSocial_02_VIEW_List(request):
    QS = a_msgSocial_02.objects.order_by('auto_citizen', 'priority')
    return a_msgSocial_02.auto_list(request, QS, vTitle = 'Personal Messages')

