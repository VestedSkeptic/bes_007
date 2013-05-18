# *********************************************************
# a_library_02/engine_paginate.py

# *********************************************************
from django.core.paginator import Paginator, InvalidPage
from django.db.models.query import QuerySet

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
class engine_paginate(object):
    
    # *********************************************************
#    def __init__(self, request, objectList, appName, paginateBy=10, urlprefix='', sortBy=[], sessionVarsUniqueIdentifier=''):
#    def __init__(self, request, objectList, appName, paginateBy=10, urlprefix='', sortBy=[]):
    def __init__(self, request, objectList, appName, paginateBy, urlprefix='', sortBy=[]):

        self.urlprefix   = urlprefix
        self.urlname     = urlnames
        self.sortBy      = sortBy

        # Find sort value
        # Priority is url Get URL value
        # Then session variable if it exists
        # Finally sortBy param if it exists
        self.sort = request.GET.get('sort', None)
        if self.sort is None:
#            self.sort = request.session.get(appName+'_sort_'+sessionVarsUniqueIdentifier)            
#            self.sort = request.session.get(appName+'_sort_')            
            self.sort = request.session.get('_sort_')   
                     
            if self.sort is None:
                if len(sortBy):
                    self.sort = sortBy[0] 
#                    print "*** sort from sortBy[0] = %s" % (self.sort)
#            else:
#                print "*** sort from session = %s" % (self.sort)
#        else: 
#            print "*** sort from url = %s" % (self.sort)
        
        if isinstance(objectList, QuerySet):
            if self.sort is not None:   self.objectList = objectList.order_by(self.sort)
            else:                       self.objectList = objectList    
        else:
            if self.sort is not None:   
                objectList.append(self.sort)                  
            # QuerysetWrapper seems to take a list and wraps so it can be treated as a Queryset
            self.objectList = QuerysetWrapper(objectList)            
            
        self.p = Paginator(self.objectList, paginateBy, orphans=0, allow_empty_first_page=True)

        # Find pageNumber
        # Priority is url Get URL value
        # Then session variable if exists
        # Finally just set it to 1
        pageNumber = request.GET.get('page', None)
        if pageNumber is None:
#            pageNumber = request.session.get(appName+'_page_'+sessionVarsUniqueIdentifier)           
#            pageNumber = request.session.get(appName+'_page_')           
            pageNumber = request.session.get('_page_')       
                
            if pageNumber is None:
                pageNumber = 1      
#                print "*** pageNumber from default = %s" % (pageNumber)
#            else:
#                print "*** pageNumber from session = %s" % (pageNumber)
#        else:
#            print "*** pageNumber from url = %s" % (pageNumber)

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

        # save sort and page value in session variable by appName
        if self.sort is not None:
#            request.session[appName+'_sort_'+sessionVarsUniqueIdentifier] = self.sort             
#            request.session[appName+'_sort_'] = self.sort             
            request.session['_sort_'] = self.sort    
                     
#        request.session[appName+'_page_'+sessionVarsUniqueIdentifier] = pageNumber              
#        request.session[appName+'_page_'] = pageNumber              
        request.session['_page_'] = pageNumber
                      
        request.session['lastPagination_appName'] = appName + '_' + request.META['auto_currentView']              

    # *********************************************************    
    def get_sortByNavigationDict(self):
        if len(self.sortBy):
            outDict = {}
            for k in self.sortBy:
                # normalized_key is the sort term without the prepended minus sign so it is good to use
                # in the template tag and in the text for the link!!!
                normalized_key = k
                if normalized_key[0] == '-':
                    normalized_key = normalized_key[1:]
                boldStartTag = ''
                boldEndTag = ''

                # detect and re-verse (wrt the minus sign) the current sort     
                sortDirection = '&uarr'; #'asc'
                if (k == self.sort):
                    if k[0] == '-': 
                        k = k[1:]
                        sortDirection = '&uarr'; #'asc'
                    else:           
                        k = '-' + k
                        sortDirection = '&darr;'; #'desc'
                        
                if (normalized_key == self.sort) or (normalized_key == self.sort[1:]):
                    outDict[normalized_key] = '<b>%s <a href="%ssort=%s">%s%s%s</a></b>' % (normalized_key, self.fix_url(self.urlprefix), k, boldStartTag, sortDirection, boldEndTag)
                else:
                    outDict[normalized_key] = '<a href="%ssort=%s">%s%s%s</a>' % (self.fix_url(self.urlprefix), k, boldStartTag, normalized_key, boldEndTag)
            return outDict
        else:
            return {}        
        
    # *********************************************************
    def fix_url(self, url):
        if url.find('?') == -1:                               url = url + '?'
        elif not url.endswith('&') and not url.endswith('?'): url = url + '&'
        return url

    # *********************************************************    
    def next_url(self):
        if self.has_next:
            if self.sort is None:    return '<a href="%spage=%d">%s</a>'         % (self.fix_url(self.urlprefix), self.next, self.urlname['next'])
            else:                    return '<a href="%spage=%d&sort=%s">%s</a>' % (self.fix_url(self.urlprefix), self.next, self.sort, self.urlname['next'])
        else:                        return ''
        
    # *********************************************************
    def previous_url(self):
        if self.has_previous:
            if self.sort is None:    return '<a href="%spage=%d">%s</a>'         % (self.fix_url(self.urlprefix), self.previous, self.urlname['previous'])
            else:                    return '<a href="%spage=%d&sort=%s">%s</a>' % (self.fix_url(self.urlprefix), self.previous, self.sort, self.urlname['previous'])
        else:                        return ''
        
    # *********************************************************
    def first_url(self):
        if self.pages > 1 and self.pageNumber != 1:
            if self.sort is None:    return '<a href="%spage=1">%s</a>'         % (self.fix_url(self.urlprefix), self.urlname['first'])
            else:                    return '<a href="%spage=1&sort=%s">%s</a>' % (self.fix_url(self.urlprefix), self.sort, self.urlname['first'])
        else:                        return ''
        
    # *********************************************************
    def last_url(self):
        if self.pages > 1 and self.pageNumber != self.pages:
            if self.sort is None:    return '<a href="%spage=%d">%s</a>'         % (self.fix_url(self.urlprefix), self.pages, self.urlname['last'])
            else:                    return '<a href="%spage=%d&sort=%s">%s</a>' % (self.fix_url(self.urlprefix), self.pages, self.sort, self.urlname['last'])
        else:                        return ''
