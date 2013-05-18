# *********************************************************
# a_library_02/e_paginate.py

# *********************************************************
from django.core.paginator import Paginator, InvalidPage
from django.db.models.query import QuerySet
import settings

# *********************************************************
urlnames = {'next':('next'), 'previous':('previous'), 'first':('first'), 'last':('last')}

# *********************************************************
class QuerysetWrapper(object):
    def __init__(self, t):
        self.list = t

    def count(self):
        return len(self.list)

    def __len__(self):
        return len(self.list)

    def __getslice__(self, i, j):
        return self.list[max(0, i):max(0, j):]

# *********************************************************
class e_paginate(object):
    
    # *********************************************************
    def __init__(self, request, contextDict, contextPaginationKey, urlprefix=''):
        self.appName     = request.META['auto_currentApp']
        self.paginateBy  = settings.PAGINATION_VALUE
        self.urlprefix   = urlprefix
        self.urlname     = urlnames
        
        objectList= contextDict.get(contextPaginationKey, [])
        
        if isinstance(objectList, QuerySet):
            self.objectList = objectList    
        else:
            # QuerysetWrapper seems to take a list and wraps so it can be treated as a Queryset
            self.objectList = QuerysetWrapper(objectList)            
            
        self.p = Paginator(self.objectList, self.paginateBy, orphans=0, allow_empty_first_page=True)

        # Find pageNumber
        # Priority is url Get URL value
        # Then session variable if exists
        # Finally just set it to 1
        pageNumber = request.GET.get('page', None)
        if pageNumber is None:
            pageNumber = request.session.get('_page_')       
                
            if pageNumber is None:
                pageNumber = 1      
###                print "*** pageNumber from default = %s" % (pageNumber)
###            else:
###                print "*** pageNumber from session = %s" % (pageNumber)
###        else:
###            print "*** pageNumber from url = %s" % (pageNumber)

        pageNumber = int(pageNumber)
        try:
            pageObj = self.p.page(pageNumber)
            objectList = pageObj.object_list
        except (InvalidPage, ValueError):
            objectList = []

        self.has_next             = pageObj.has_next()
        self.has_previous         = pageObj.has_previous()
        self.pageNumber           = pageNumber
        self.next                 = pageNumber + 1
        self.previous             = pageNumber - 1
        self.pages                = self.p.num_pages
        self.objectList           = objectList
        self.paginatedListFound   = False
        if self.pages > 1:
            self.paginatedListFound = True

        request.session['_page_'] = pageNumber
        request.session['lastPagination_appName'] = self.appName + '_' + request.META['auto_currentView']              

    # *********************************************************
    def fix_url(self, url):
        if url.find('?') == -1:                               url = url + '?'
        elif not url.endswith('&') and not url.endswith('?'): url = url + '&'
        return url

    # *********************************************************    
    def next_url(self):
        if self.has_next:           return '<a href="%spage=%d">%s</a>'         % (self.fix_url(self.urlprefix), self.next, self.urlname['next'])
        else:                       return ''
        
    # *********************************************************
    def previous_url(self):
        if self.has_previous:       return '<a href="%spage=%d">%s</a>'         % (self.fix_url(self.urlprefix), self.previous, self.urlname['previous'])
        else:                       return ''
        
    # *********************************************************
    def first_url(self):
        if self.pages > 1 and self.pageNumber != 1:     return '<a href="%spage=1">%s</a>'         % (self.fix_url(self.urlprefix), self.urlname['first'])
        else:                                           return ''
        
    # *********************************************************
    def last_url(self):
        if self.pages > 1 and self.pageNumber != self.pages:        return '<a href="%spage=%d">%s</a>'         % (self.fix_url(self.urlprefix), self.pages, self.urlname['last'])
        else:                                                       return ''
