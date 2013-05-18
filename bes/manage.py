#!/usr/bin/env python
from django.core.management import execute_manager
try:
    import sys
    import settings
    
    sys.path.append(settings.SYS_PATH_APPEND1)
    sys.path.append(settings.SYS_PATH_APPEND2)
    if not settings.HOSTED_ONLINE:
        sys.path.append(settings.SYS_PATH_APPEND3)      
        
except ImportError:
    import sys
    sys.stderr.write("Error: manage.py - Can't find the file 'settings.py'")
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)