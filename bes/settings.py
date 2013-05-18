PROJECT_NAME    = 'bes_007'

HOSTED_SRC_DIR  = '/home/molw/webapps/django/'+PROJECT_NAME+'/bes'           
HOSTED_LIB_DIR  = '/home/molw/webapps/django/'+PROJECT_NAME+'/library'       

LOCAL_SRC_DIR   = 'D:\\github\\'+PROJECT_NAME+'\\bes'    
LOCAL_LIB_DIR   = 'D:\\github\\'+PROJECT_NAME+'\\library'           

try:
    fp = open(HOSTED_SRC_DIR+'/HOSTED_ONLINE.cfg', 'r')
    fp.close()
    HOSTED_ONLINE  = True
    from settings_web import *
except IOError:
    HOSTED_ONLINE  = False
    from settings_local import *

VERSION_MAJOR                   = 0
VERSION_MINOR_1                 = 0
VERSION_MINOR_2                 = 71
    
#HOME_VIEW                       = 'd_premises_02_VIEW_home'    
#HOME_VIEW                       = 'd_contracts_02_VIEW_home'    
# HOME_VIEW                       = 'd_eve_02_VIEW_home'    
HOME_VIEW                       = 'd_move_02_VIEW_home'    
MEDIA_PRJ                       = 'bes_media_007'
MEDIA_LIB                       = 'lib_media_007'
MEDIA_URL                       = ''.join(['/',MEDIA_LIB,'/'])
INTERNAL_IPS                    = (SITE_URL)
DIRECT_HTTP_HOST                = SITE_URL
    
if HOSTED_ONLINE:
    DEBUG                       = False
    SRC_DIR                     = HOSTED_SRC_DIR
    LIB_DIR                     = HOSTED_LIB_DIR
    SYS_PATH_APPEND1            = HOSTED_SRC_DIR  
    SYS_PATH_APPEND2            = HOSTED_LIB_DIR    
    EMAIL_HOST                  = 'smtp3.webfaction.com'
    EMAIL_HOST_USER             = 'besomeone'
    EMAIL_HOST_PASSWORD         = 'ABCDQWER17'
    EMAIL_PORT                  = 25
    EMAIL_USE_TLS               = False
    DEFAULT_FROM_EMAIL          = 'donotreply@besomeone.ca'
    CACHE_TIME_IN_SECONDS       = 3600
else:
    DEBUG                       = True
    SRC_DIR                     = LOCAL_SRC_DIR   
    LIB_DIR                     = LOCAL_LIB_DIR
    SYS_PATH_APPEND1            = LOCAL_SRC_DIR  
    SYS_PATH_APPEND2            = "D:\\rational files\\Python\\Lib\\site-packages\\django-extensions"
    SYS_PATH_APPEND3            = LOCAL_LIB_DIR
    EMAIL_HOST                  = 'smtp.gmail.com'
    EMAIL_HOST_PASSWORD         = 'QWERABCD21'
    EMAIL_HOST_USER             = 'ReluctantStranger@gmail.com'
    EMAIL_PORT                  = 587
    EMAIL_USE_TLS               = True
    DEFAULT_FROM_EMAIL          = 'ReluctantStranger@gmail.com'
    CACHE_TIME_IN_SECONDS       = 10

try:
    if HOSTED_ONLINE: fp = open(HOSTED_SRC_DIR+'/WEBSITE_IS_DOWN.html', 'r')
    else:             fp = open(LOCAL_SRC_DIR+'/WEBSITE_IS_DOWN.html', 'r')
    fp.close()
    WEBSITE_IS_DOWN  = True
except IOError:
    WEBSITE_IS_DOWN  = False    
    
CACHE_BACKEND                   = 'db://cache_table'             #CACHE_BACKEND  = 'db://cache_table/?max_entries=4000'            
ROOT_URLCONF                    = 'urls_direct'
HOST_MIDDLEWARE_URLCONF_MAP     = {FACEBOOK_HTTP_HOST[:-5]: "urls_fb"}
DATABASE_ENGINE	 	            = 'postgresql_psycopg2'
DATABASE_HOST 		            = ''
DATABASE_PORT 		            = ''
VERSION_NUMBER                  = float(VERSION_MAJOR.__str__() + '.' + VERSION_MINOR_1.__str__() + VERSION_MINOR_2.__str__())
TEMPLATE_DEBUG                  = DEBUG
AUTHOR_ID                       = 1
GOOGLE_API_KEY                  = 'ABQIAAAAfFwfVH9X62j3aiFtxWnHwBTpH3CbXHjuCVmaTc5MkkU4wO1RRhSb_6CEsYYno2pVv-cxwNO6b4DzNg'
LOGIN_URL                       = '/'                                              # Destination URL for views using the login_required decorator when the user is not logged in  
ADMINS                          = (('exception', 'ReluctantStranger@gmail.com'),)       # When DEBUG is False these people will be emailed full exception information
MANAGERS                        = ADMINS
TIME_ZONE                       = 'America/Montreal'
SITE_ID                         = 3
USE_I18N                        = True
SECRET_KEY                      = 'a7=alr^opp*s(jywe$l^uulx7h(lny-@%w4kc_7ejovvo-p0_6'     # Make this unique, and don't share it with anybody.
MIN_PASSWORD_LENGTH             = 4
SITE_ADMIN_EMAIL                = 'ReluctantStranger@gmail.com'    
ADMIN_MEDIA_PREFIX              = '/adminMedia/'   
MAXIMUM_VIEW_HISTORY            = 4

PAGINATION_VALUE                = 10

TAGCLOUD_STEPS                  = 4             # 4
TAGCLOUD_MINCOUNT               = 1             # 1

# django tagging settings
FORCE_LOWERCASE_TAGS            = False
MAX_TAG_LENGTH                  = 50

DEV_DIRECT_UID                  = 527106161            # ME

MEDIA_ROOT                      = LIB_DIR+'/media_files/'

# -------------------------------------------------
COMPRESS_AUTO           = False          # True if I want a new compressed file generated every time
COMPRESS                = True
COMPRESS_VERSION        = True
CSSTIDY_ARGUMENTS       = '--template=highest --silent=true' 
#COMPRESS_CSS_FILTERS    = ()            # to disable csstidy

COMPRESS_CSS        = {
    'group_one_css': {
        'source_filenames'  : ('css/reset-fonts-grids.css', 'css/typography.css', 'css/grid.css', 'css/forms.css', 'css/library_styles.ccss',),
        'output_filename'   : 'css/xcomp_c.r?.css',
        'extra_context'     : {'media': 'screen,projection',},
    },
    'group_two_css': {
        'source_filenames'  : ('css2/reset-fonts-grids.css', 'css2/typography.css', 'css2/grid.css', 'css2/forms.css', 'css2/my_styles.ccss',),
        'output_filename'   : 'css2/xcomp_c2.r?.css',
        'extra_context'     : {'media': 'screen,projection',},
    },
    # other CSS groups goes here
}
COMPRESS_JS         = {
    'all_js': {
        'source_filenames'  : ('javascript/jquery-1.2.6.js', 'javascript/besomeone.js', 'javascript/a_discussion_01.js',),
        'output_filename'   : 'javascript/xcomp_j.r?.js',
    }
}
# FOR DJANGO_CSS
COMPILER_FORMATS = {
        '.sass': {
            'binary_path':'sass',
            'arguments': 'SOURCE_FILENAME.sass SOURCE_FILENAME.css'
        },
        '.hss': {
            'binary_path':'/home/dziegler/hss',
            'arguments':'SOURCE_FILENAME.hss'
        },
        '.ccss': {
            'binary_path':'D:\\RATION~1\\Python\\Lib\\SITE-P~1\\clevercss',
            'arguments':'SOURCE_FILENAME.ccss'
        },
    }

# -------------------------------------------------

TEMPLATE_DIRS = (
    SRC_DIR,
    SRC_DIR+"/templates",
    LIB_DIR,
    LIB_DIR+"/templates",    
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',    
)
    
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'facebook.djangofb.FacebookMiddleware',
    'a_mgrMiddleWare_02.models.a_mgrMiddleWare_02',                         
)

INSTALLED_APPS = (
    'django_extensions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django_css',
    'tagging',
    'a_base_02',
    'a_citizen_02',
    'a_library_02',
    'a_mgrApplication_03',
    'a_mgrEmail_02',
    'a_mgrSidebar_02',
    'a_msgSocial_02',
    'a_msgUser_02',
    'a_update_02',
    'a_mgrCache_01',
    'a_mgrVerHistory_01',
    'c_nav_02',
    'e_thread_03',
    'd_move_02',
)