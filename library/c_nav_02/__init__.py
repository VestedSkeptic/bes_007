    
###    # -----------------------------------------------------
###    def mw_view_navMenu(request, view_func, view_args, view_kwargs):
###        parentIndicatedAsSelectedByFoundChildSelected       = ''
###        ultimateProperParentSelectedList                    = []
###        
###        # First extract appropriate child entries
###        if navMenu_localDict.has_key(request.META['auto_currentApp_baseName']):
###            for menuType, menuList in navMenu_localDict[request.META['auto_currentApp_baseName']].items():
###
###                # get all child entries for the currentApp current menuType (i.e. LOCAL)
###                working_childMenuList           = []
###                aLocalChildWasFoundSelectedAndItsParentIs    = ''
###                for x in menuList:
###                    if engine_permissions.checkUserPermissions(request.META['citizen_rights'], x[2], view_args, view_kwargs, request):
###                        working_childMenuList.insert(0, x)
###                        if x[2] == request.META['auto_currentView']:
###                            aLocalChildWasFoundSelectedAndItsParentIs = x[5]
###                    
###                # extract entries which have the properParent we are looking for        
###                final_working_childMenuList = []
###                if working_childMenuList:
###                    if aLocalChildWasFoundSelectedAndItsParentIs:    properParent = aLocalChildWasFoundSelectedAndItsParentIs
###                    else:                               properParent = request.META['auto_currentView']
###                    if properParent not in ultimateProperParentSelectedList:
###                        ultimateProperParentSelectedList.append(properParent)
###                    
###                    for x in working_childMenuList:
###                        if x[2] == request.META['auto_currentView']:  
###                            x[4] = True
###                            final_working_childMenuList.insert(0, x)
###                        elif x[5] == properParent:                       
###                            x[4] = False
###                            final_working_childMenuList.insert(0, x)
###                        
###                if final_working_childMenuList:
###                    final_working_childMenuList.sort()
###                    # ----------------                           
#####                    try:
#####                        if x[6]:
#####                            print "*** CHILD menu item has a render method but this isn't implemented yet. See how the parent is done especially how the templates need to be changed to manage one object at a time rather then be passed a list"
#####                        templateName = 'BLOCK_menu_%s.html'%(menuType)
#####                        request.META['baseContext_navigationMenu_%s' % (menuType)] = c_nav_02.processTemplate_01(request, templateName, {'objectList': final_working_childMenuList})
#####                    except TemplateDoesNotExist:
#####                        request.META['baseContext_navigationMenu_%s' % (menuType)] = "ERROR: %s does not exist" % (templateName)                                 
###                    # ----------------                           
###                    renderedList = []
###                    for x in final_working_childMenuList:
###                        
###                        if x[7]: # there is a displayCriteriaMethod name, use it to get the actual method from the class
###                            classObj = registeredClassInfo.get_classObject_fromBaseName('c_nav')
###                            displayCriteriaMethod = getattr(classObj, x[7])
###                            displayCriteriaOk = displayCriteriaMethod(request)
###                        else:
###                            displayCriteriaOk = True
###                        
###                        if displayCriteriaOk:
###                            if x[6]: # there is a renderMethod name, use it to get the actual method from the class
###                                classObj = registeredClassInfo.get_classObject_fromBaseName(x[8])
###                                renderMethod = getattr(classObj, x[6])
###                                renderedList.append(renderMethod(request))
###                            else:
###                                try:
###                                    templateName = 'BLOCK_menu_%s.html'%(menuType)
###                                    renderedList.append(c_nav_02.processTemplate_01(request, templateName, {'object': x}))
###                                except TemplateDoesNotExist:
###                                    renderedList.append("ERROR: %s does not exist" % (templateName))    
###                    request.META['baseContext_navigationMenu_%s' % (menuType)] = ''.join(renderedList)  
###                    # ----------------                           
###
###        # Next check non-child entries for a selection match
###        for menuType, menuList in navMenu_globalDict.items():
###            working_nonChildMenuList  = []
###            
###            # for application menu items only display the ones a user has subscribed to (guests see all of them they have sufficient rights for)
###            if menuType == 'APP' and request.META['duo_citizen']:
###                # get a list of applications citizen is subscribed to
###                subList = []
###                QS = subscription_01.objects.filter(auto_citizen__exact=request.META['duo_citizen'])
###                for x in QS:
###                    subList.append(x.application.homeview)
###
###                # for items in MAIN menuList keep the ones the user is subscribed to
###                for x in menuList:
###                    if (x[2] in subList or x[2] == 'w_base_03_VIEW_home') and engine_permissions.checkUserPermissions(request.META['citizen_rights'], x[2], view_args, view_kwargs, request):
###                        working_nonChildMenuList.insert(0, x)
###            else:
###                for x in menuList:
###                    if engine_permissions.checkUserPermissions(request.META['citizen_rights'], x[2], view_args, view_kwargs, request):
###                        working_nonChildMenuList.insert(0, x)
###
###            if working_nonChildMenuList:
###                for x in working_nonChildMenuList:
###                    if x[5] == request.META['auto_currentApp_baseName'] and x[2] == request.META['auto_currentView'] : x[4] = True
###                    elif x[2] in ultimateProperParentSelectedList:                                                     x[4] = True
###                    else:           
###                        # New-ish conditional here testing if the optional list in x[6] contains the basename and current view. 
###                        # This optional list was added April 27 and is defined in class.models and contains all the views for which this global button shoudl be selected on.
###                        if x[5] == request.META['auto_currentApp_baseName'] and request.META['auto_currentView'] in x[6]  : x[4] = True
###                        else:                                                                                               x[4] = False
###
###                working_nonChildMenuList.sort()
###                
###                renderedList = []
###                for x in working_nonChildMenuList:
###                    
###                    if x[8]: # there is a displayCriteriaMethod name, use it to get the actual method from the class
###                        classObj = registeredClassInfo.get_classObject_fromBaseName('c_nav')
###                        displayCriteriaMethod = getattr(classObj, x[8])
###                        displayCriteriaOk = displayCriteriaMethod(request)
###                    else:
###                        displayCriteriaOk = True
###                    
###                    if displayCriteriaOk:
###                        if x[7]: # there is a renderMethod name, use it to get the actual method from the class
###                            classObj = registeredClassInfo.get_classObject_fromBaseName(x[5])
###                            renderMethod = getattr(classObj, x[7])
###                            renderedList.append(renderMethod(request))
###                        else:
###                            try:
###                                templateName = 'BLOCK_menu_%s.html'%(menuType)
###                                renderedList.append(c_nav_02.processTemplate_01(request, templateName, {'object': x}))
###                            except TemplateDoesNotExist:
###                                renderedList.append("ERROR: %s does not exist" % (templateName))    
###                request.META['baseContext_navigationMenu_%s' % (menuType)] = ''.join(renderedList)                             
###
###        return None  
###    mw_view_navMenu = staticmethod(mw_view_navMenu)