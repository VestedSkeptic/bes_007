# *********************************************************
# a_update_02/views.py

# *********************************************************
from django.contrib.contenttypes.models import ContentType
from django.core.management import execute_manager
from django.db import connection
#from a_base_02.models import allClassesDict
from a_update_02.models import a_update_02, Form_a_update_02
import inspect
import os
import settings
import sys
import time

NotePrependString = "// Note: "

# *********************************************************
def parseFile(filename, noteOnly=False):
    returnDict = {}

    instanceFieldCount          = {}
    
    returnDict['classes']       = {}
    returnDict['noteToDisplay'] = ''
    
    itemCountIndex = 0
    noteNotFound = True
    
    os.chdir(settings.SRC_DIR)
    fp = open("scripts//"+filename, mode='r')
    for origLine in fp:
        line = origLine.strip()
        
        # Test for NOTE line
        if noteNotFound and len(line) > len(NotePrependString) and line[:len(NotePrependString)] == NotePrependString:
            returnDict['noteToDisplay'] = line[len(NotePrependString):]
            noteNotFound = False
            
        # If past the generic crap before the run command
        else:
            if line[:9] == '"model": ':
                splitList = (line[9:]).split('.',1)
                
                # To handle fact that contenttype is now in json script being parsed and the
                # contenttype fields actually has a model field (ex "model": "engine_categorymanager_a", )
                # which we have to ignore
                if len(splitList) > 1:  
                    fullModelName        = splitList[0][1:]            # ex: django.contrib.auth.models, django.contrib.sessions.models, engine_urlEmailValidation_a.models
                    nonStandardClassName = splitList[1][:-2]            # ex: User, Session, engine_urlEmailValidation_a
                    
                    if nonStandardClassName in returnDict['classes']:
                        returnDict['classes'][nonStandardClassName]['importCount'] = returnDict['classes'][nonStandardClassName]['importCount'] + 1 
                    else:
                        returnDict['classes'][nonStandardClassName] = {'fullModelName':fullModelName, 'importCount':1, 'instCount':0, 'nonStandardClassName':nonStandardClassName, 'fieldCount':0}

        # Break out of here to avoid processing the rest of the file if we are just getting the note
        if noteOnly and returnDict['noteToDisplay']: break
        
    fp.close()
        
    return returnDict

# *********************************************************
def a_update_02_VIEW_List(request):
    outList=[]

    # Set directory to source directory. Not necessary on Windows but seems to be on Webfaction/Linux
    os.chdir(settings.SRC_DIR)
   
    fileList = os.listdir('scripts')
    fileList.sort()
    for x in fileList:
        if x[:5] == 'dump_' and x[-5:] ==".json":
            pfDict = parseFile(x, noteOnly=True)
            noteToDisplay = pfDict['noteToDisplay']
            outList.append([x[5:-5], noteToDisplay, x])
            
    return a_update_02.auto_list(request, outList, paginateBy=25)

# *********************************************************
def a_update_02_VIEW_Add(request):
    fn_dict = {'success' : AddEdit_processSuccess}
    return a_update_02.auto_addEdit(request, Form_a_update_02, fn_dict, None)

# *********************************************************
def AddEdit_processSuccess(*args):
    # args[0] = i (the instance)
    # args[1] = request
    # args[2] = cleanDataDict
    # args[3] = redirectReason ('edit' or 'add')    

    # NEW - July 22, 2009 - clear expired sessions from the database
    execute_manager(settings, ['manage.py','cleanup'])
    
#    dumpScriptList = ['manage.py','dumpdata','--indent=4', '--exclude=contenttypes']
#    dumpScriptList = ['manage.py','dumpdata','--indent=4']
    dumpScriptList = ['manage.py','dumpdata','--indent=4']
    
#    python2.5 manage.py dumpdata --indent=4 --exclude=auth --exclude=contenttypes > fromWF.json
#    python2.5 manage.py dumpdata --indent=4 --exclude=contenttypes > fromWF.json
#    python2.5 manage.py dumpdata --indent=4 --exclude=contenttypes > scripts\fromWF.json
    
    timeX = "%s" % (time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time())))
    fileName = "dump_" + timeX + ".json"
    
    # exec_manager doesn't actually return anything that I can store. It seems to automatically display it to the
    # command window. Therefore to capture it I need to temporarily redirecty sys.stdout to my file
    os.chdir(settings.SRC_DIR)
    fp = open("scripts//"+fileName, mode='w')

    # First write note to the top of the file
    fp.write(NotePrependString)
    fp.write(args[2]['note'])
    fp.write('\n')

    tempSavedOut = sys.stdout
    sys.stdout = fp 
    execute_manager(settings, dumpScriptList)
    sys.stdout = tempSavedOut
    
    fp.close()    

# *********************************************************
def getClassList_fromParsedFile(scriptName):
    classList = []
    parsedFileDict = parseFile(scriptName)
    
    for key, value in parsedFileDict['classes'].items():
        if value['fullModelName'] not in classList:
            classList.append(value['fullModelName'])
    classList.sort()
    return classList

# *********************************************************
def generateTempCommentFreeJsonFile(scriptName):
    os.chdir(settings.SRC_DIR)

    origFP = open("scripts//"+scriptName, mode='r')
    tempFP = open("scripts//temp.json", mode='w')
    
    firstLineSkipped = False
        
    for line in origFP:
        if not firstLineSkipped:    firstLineSkipped = True
        else:                       tempFP.write(line)

    origFP.close()
    tempFP.close()
    

# *********************************************************
def a_update_02_VIEW_ResetTo(request, scriptName):
    # reset_cascade is a custom copy (look in engine_LIBRARY_a/management/commands) of the reset command. 
    # This one forces the drop table command to cascade setting them back to empty irregardless of
    # foreign keys.
    
#    resetScriptList = ['manage.py','reset_cascade']
    resetScriptList = ['manage.py','reset_cascade']
    parsedClassList = getClassList_fromParsedFile(scriptName)
    resetScriptList = resetScriptList + parsedClassList
    resetScriptList.append('--noinput')
    execute_manager(settings, resetScriptList)

#    syncScriptList = ['manage.py','syncdb','--noinput']
#    syncScriptList = ['manage.py','syncdb','--noinput']
#    execute_manager(settings, syncScriptList)

#    runScriptList = ['manage.py','loaddata', "scripts//"+scriptName]
#    runScriptList = ['manage.py','loaddata', "scripts//"+scriptName]
    generateTempCommentFreeJsonFile(scriptName)     # generates scripts/temp.json which is a copy of scriptName except the first line (which is a comment) is removed.
#    runScriptList = ['manage.py','loaddata', "scripts//temp.json"]
    runScriptList = ['manage.py','loaddata', "scripts//temp.json"]
    execute_manager(settings, runScriptList)

#    syncScriptList = ['manage.py','syncdb','--noinput']
    syncScriptList = ['manage.py','syncdb','--noinput']
    execute_manager(settings, syncScriptList)
    
    # delete cachetable if it exists
    cursor = connection.cursor()
    sqlString = "DROP TABLE IF EXISTS %s" % (settings.CACHE_BACKEND[5:])
    cursor.execute(sqlString)
    
    # create cachetable
#    cctScriptList = ['manage.py', 'createcachetable', settings.CACHE_BACKEND[5:]]
    cctScriptList = ['manage.py', 'createcachetable', settings.CACHE_BACKEND[5:]]
    execute_manager(settings, cctScriptList)
    
    return a_update_02.redirectView(request, 'a_update_02_VIEW_List', 'update')

# *********************************************************
def a_update_02_VIEW_Contents(request, scriptName):
    contextDict = {}
    objInfo=[]
    parsedFileDict = parseFile(scriptName)
    objInfo.append([scriptName[5:-5], parsedFileDict['noteToDisplay'], scriptName])
    
    # convert the rest of parsedFileDict to a list I can sort for a nicer display
    sortedList = []
    if parsedFileDict['classes']:
        for k, v in parsedFileDict['classes'].items():
            tempList = [v['fullModelName'], v['nonStandardClassName'], v['importCount'], v['fieldCount'], v['instCount']]
            if 'errorFound' in v:
                tempList.append(v['errorFound'])
            sortedList.append(tempList)
    sortedList.sort()
    
    contextDict['main_1'] = a_update_02.processTemplate_01(request, request.META['auto_currentApp']+'/templates/BLOCK_Contents.html', {'objInfo': objInfo, 'sortedList':sortedList})
    return a_update_02.processTemplate_01(request, 'BASE.html', contextDict, mode='view')