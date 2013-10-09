from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prototype.views.home', name='home'),
    # url(r'^prototype/', include('prototype.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'user_status.views.show_root', name='root_page'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login_page'),
    url(r'^logout/$', 'user_status.views.logout_user', name='logout_page'),
    url(r'^create_group_page/$', 'group_info.views.create_group', name='create_group_page'),
    url(r'^group_page/(?P<group_info_id>\d+)/$', 'group_info.views.show_group_page', name='group_page'),
    url(r'^group_list_page/$', 'group_info.views.show_group_list', name='group_list_page'),
    url(r'^group_management_page/(?P<group_info_id>\d+)/$', 'group_info.views.show_group_management', name='group_management_page'),
    url(r'^group_management_page/delete_user/$', 'group_info.views.delete_user_from_group', name='delete_user_from_group'),
    url(r'^group_management_page/remove_manager/$', 'group_info.views.remove_user_from_group_manager', name='delete_manager_from_group'),
    url(r'^create_project_page/$', 'project_info.views.create_project', name='create_project_page'),
    url(r'^project_page/(?P<project_info_id>\d+)/$', 'project_info.views.show_project_page', name='project_page'),
    url(r'^project_list_page/$', 'project_info.views.show_project_list', name='project_list_page'),
    
)
