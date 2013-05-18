# *********************************************************
# urls_fb.py

# *********************************************************
import settings
from urls_base import generateUrlPatterns

if settings.HOSTED_ONLINE: urlPrefix = 'besomeone/'
else:                      urlPrefix = 'duo_boycott_d/'

urlpatterns = generateUrlPatterns(urlPrefix)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'