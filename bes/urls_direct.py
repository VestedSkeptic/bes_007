# *********************************************************
# urls_direct.py

# *********************************************************
import settings
from urls_base import generateUrlPatterns

urlPrefix = ''

urlpatterns = generateUrlPatterns(urlPrefix)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'