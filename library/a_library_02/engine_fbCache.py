# *********************************************************
# a_library_02/engine_fbCache.py

from django.core.cache import cache
from facebook import FacebookError

#fbTimeout_24Hours = 60*60*24
#fbTimeout_24Hours = 60*60    # one hour for now
fbTimeout_24Hours = 60*60*4    # four hours

#allFields = "about_me, activities, affiliations, birthday, books, current_location, education_history, email_hashes, first_name, has_added_app, hometown_location, hs_info, interests, is_app_user, last_name, locale, meeting_for, meeting_sex, movies, music, name, notes_count, pic, pic_big, pic_small, pic_square, political, profile_update_time, profile_url, proxied_email, quotes, relationship_status, religion, sex, significant_other_id, status, timezone, tv, wall_count, work_history"
#allFields = "about_me, activities, affiliations, birthday, books, current_location, education_history, first_name, has_added_app, hometown_location, hs_info, interests, is_app_user, last_name, locale, meeting_for, meeting_sex, movies, music, name, notes_count, pic, pic_big, pic_small, pic_square, political, profile_update_time, quotes, relationship_status, religion, sex, significant_other_id, status, timezone, tv, wall_count, work_history"
allFields = "about_me,activities,affiliations,birthday,books,current_location,education_history,first_name,has_added_app,hometown_location,hs_info,interests,is_app_user,last_name,locale,meeting_for,meeting_sex,movies,music,name,notes_count,pic,pic_big,pic_small,pic_square,political,profile_update_time,quotes,relationship_status,religion,sex,significant_other_id,status,timezone,tv,wall_count,work_history"

fieldNotFoundToken = 'z. not found'

# *********************************************************
def getFriendListCacheKey(request):
    return "userFriendList_"+request.POST['fb_sig_user']

# *********************************************************
def getUserInfoCacheKey(request, uid):
    return "userInfo_"+uid.__str__()

# *********************************************************
def getFriendList(request):
    cacheKey = getFriendListCacheKey(request)

    uidList = cache.get(cacheKey)
    if uidList is None:
        print "*** cacheKey '%s' not found in cache. Getting from FB and then storing it in cache." % (cacheKey)
        uidList = request.facebook.friends.get()
        cache.set(cacheKey, uidList, fbTimeout_24Hours)
    return uidList

# *********************************************************
def getInfo_friends(request, fieldList=[]):
    uidList = getFriendList(request)
    returnValue = getInfo_uidList(request, uidList, fieldList)
    return returnValue

# *********************************************************
def getInfo_friendsAndMe(request, fieldList=[]):
    uidList = getFriendList(request)
    uidList.insert(0, request.POST['fb_sig_user'])
    returnValue = getInfo_uidList(request, uidList, fieldList)
    return returnValue

## *********************************************************
def getInfo_uidList(request, uidList, fieldList=[]):
    returnList = []
    
    print "*** getInfo_uidList: this method being phased out use %s instead" % ('getUserData')
    
    if uidList:
        FULL_uidListCount = len(uidList)

        # generate list of cacheKeys to check and then get_many them out of the cache
        cacheKeyList = []
        for x in uidList:
            cacheKeyList.append(getUserInfoCacheKey(request, x))
        cachedEntriesDict = cache.get_many(cacheKeyList)
        
        # FIRST TRY AND GET ITEMS FROM THE CACHE
        # For items retrieved from cache
        for key, value in cachedEntriesDict.items():
            try:
                # Eliminate appropriate uid from uidList so it isn't retrieved from FaceBook below
                uidList.remove("%s" % (value['uid']))
            except ValueError, e:
                print e
                pass
            
            # Extract the appropriate  data to be returned and put it into returnList
            localDict = {}    
            localDict['uid'] = value['uid']
            for z in fieldList:
                if z in value:
                    localDict[z] = value[z]
            returnList.append(localDict)
            
        # NEXT GET ANY REMAINING ITEMS FROM FB and cache them for next time 
        UNCACHED_uidListCount = len(uidList)
        if uidList:
            # generate string representing uid's for WHERE clause
            uidListString = ''
            count = 0
            for x in uidList:
                if count: uidListString += ', '
                uidListString += x
                count += 1
            
            queryString = "SELECT uid, %s FROM user WHERE uid IN (%s)" % (allFields, uidListString) 

            try:
                fugiList = request.facebook.fql.query(queryString)
                
                # For items retrieved from FACEBOOK
                for value in fugiList:
                    # CACHE IT
                    cache.set(getUserInfoCacheKey(request, value['uid']), value, fbTimeout_24Hours)

                    # Extract the appropriate fieldList data to be returned and put it into returnList
                    localDict = {}    
                    localDict['uid'] = value['uid']
                    for z in fieldList:
                        localDict[z] = value[z]
                    returnList.append(localDict)
            except FacebookError, e:
                print "ERROR: '%s' for queryString '%s'" % (e, queryString)
        
        if UNCACHED_uidListCount:
            print "*** getInfo_uidList: %s of %s entries were retrieved from FaceBook, the rest retrieved from cache" % (UNCACHED_uidListCount, FULL_uidListCount)

    return returnList

## *********************************************************
def getUserData(request, uidList, fieldList=[], skipCache=False):
    returnDict = {'found':[]}

    if not fieldList:  fieldList = allFields.split(",")
    
    if uidList and not skipCache:
        # generate list of cacheKeys to check and then get_many them out of the cache
        cacheKeyList = []
        for x in uidList:
            cacheKeyList.append(getUserInfoCacheKey(request, x))
        cachedEntriesDict = cache.get_many(cacheKeyList)
        
        for key, value in cachedEntriesDict.items():
            try:
                uidList.remove("%s" % (value['uid']))   # Eliminate appropriate uid from uidList so it isn't retrieved from FaceBook below
            except ValueError, e:
                print e
            
            # Extract the appropriate data to be returned
            localDict = {}    
            localDict['uid'] = value['uid']
            localDict['cached'] = True
            for z in fieldList:
                if z in value:  localDict[z] = value[z]
                else:           localDict[z] = fieldNotFoundToken
            returnDict['found'].append(localDict)
                
    # NEXT GET ANY REMAINING ITEMS FROM FB and cache them for next time 
    if uidList:
        uidListString = ', '.join(uidList)
        queryString = "SELECT uid,%s FROM user WHERE uid IN (%s)" % (allFields, uidListString)
        
        try:
            fugiList = request.facebook.fql.query(queryString)
        except FacebookError, e:
            print "ERROR: '%s' for queryString '%s'" % (e, queryString)
            
        # For items retrieved from FACEBOOK
        for value in fugiList:
            cache.set(getUserInfoCacheKey(request, value['uid']), value, fbTimeout_24Hours)  # CACHE IT

            # Extract the appropriate data to be returned
            localDict = {}    
            localDict['uid'] = value['uid']
            for z in fieldList:
                if z in value:  localDict[z] = value[z]
                else:           localDict[z] = fieldNotFoundToken
            returnDict['found'].append(localDict)
            
            # remove uid just retrieved from uidList so at the end the remaining ones are items that weren't cached or returned from FB
            try:
                uidList.remove("%s" % (value['uid']))
            except ValueError, e:
                print e
                
        # uids in uidList didn't return any values from cache (possibly skipped - verify) or Facebook
        returnDict['notfound'] = uidList

    return returnDict
