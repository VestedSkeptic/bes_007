# *********************************************************
# urls_base.py

from django.conf.urls.defaults     import include, patterns, url
import settings

# *********************************************************
def generateUrlPatterns(urlPrefix):

    if settings.WEBSITE_IS_DOWN:
        urlPrefix += "wis_"
            
    urlpatterns = patterns('old/',
                                                            ###        (r'^'+urlPrefix+'w_base_03/',                      include('w_base_03.urls')),
                                                            ###        (r'^'+urlPrefix+'admin/friends/',                  include('a_friends_01.urls')),
                                                            ###        (r'^'+urlPrefix+'admin/mgrPublish/',               include('a_mgrPublish_02.urls')),
                                                            ###        (r'^'+urlPrefix+'admin/releaseHistory/',           include('c_releaseHistory_02.urls')),
                                                            ###        (r'^'+urlPrefix+'older/entry/',                          include('e_entry_03.urls')),
                                                            ###        (r'^'+urlPrefix+'older/problems/',                       include('v_problems_01.urls')),
                                                            ###        (r'^'+urlPrefix+'older/solutions/',                      include('v_solutions_01.urls')),
                                                            ###        (r'^'+urlPrefix+'older/mafia2/',                         include('v_mafiagame_02.urls')),
                                                            ###        (r'^'+urlPrefix+'old/',                                include('p_base_01.urls')),
                                                            ###        (r'^'+urlPrefix+'old/',                                include('p_article_01.urls')),
                                                            ###        (r'^'+urlPrefix+'old/',                                include('p_info_01.urls')),
                                                            ###        (r'^'+urlPrefix+'old/',                                include('p_problem_01.urls')),       # THIS HAS TO BE THE LAST OF THE p_* modules       
                                                            ####        (r'^'+urlPrefix+'twitter/',                                 include('d_twitter_01.urls')),       
        (r'^'+urlPrefix+'citizen/',                         include('a_citizen_02.urls')),
        (r'^'+urlPrefix+'admin/mgrApplications/',           include('a_mgrApplication_03.urls')),
##        (r'^'+urlPrefix+'admin/mgrCategories/',             include('a_mgrCategories_02.urls')),
        (r'^'+urlPrefix+'admin/mgrEmail/',                  include('a_mgrEmail_02.urls')),
        (r'^'+urlPrefix+'admin/msgSocial/',                 include('a_msgSocial_02.urls')),
        (r'^'+urlPrefix+'admin/msgUser/',                   include('a_msgUser_02.urls')),
        (r'^'+urlPrefix+'admin/update/',                    include('a_update_02.urls')),
        (r'^'+urlPrefix+'thread/',                          include('e_thread_03.urls')),
##        (r'^'+urlPrefix+'comment/',                         include('c_comment_03.urls')),
##        (r'^'+urlPrefix+'blog/',                            include('d_blog_01.urls')),       
# #         (r'^'+urlPrefix+'',                                 include('d_premises_02.urls')),       
# #         (r'^'+urlPrefix+'definition/',                      include('d_definition_02.urls')),       
# #         (r'^'+urlPrefix+'questions/',                       include('d_questions_01.urls')),       
# #         (r'^'+urlPrefix+'momentous/',                       include('d_momentous_02.urls')),       
###        (r'^'+urlPrefix+'contracts/',                       include('d_contracts_02.urls')),       
# #         (r'^'+urlPrefix+'eve/',                             include('d_eve_02.urls')),       
        (r'^'+urlPrefix+'move/',                            include('d_move_02.urls')),       
    )
    
    if not settings.HOSTED_ONLINE:
        urlpatterns += patterns('',
            (r'^'+settings.MEDIA_PRJ+'/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.SRC_DIR+'/media_files'}),
            (r'^'+settings.MEDIA_LIB+'/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.LIB_DIR+'/media_files'}),            
        )
    
    return urlpatterns
    
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'