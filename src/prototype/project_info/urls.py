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
    url(r'^create/$', 'project_info.views.create_project', name='create_project_page'),
    url(r'^list/$', 'project_info.views.show_project_list', name='project_list_page'),
    url(r'^group_of_project/(?P<project_info_id>\d+)/$', 'project_info.views.show_project_page', name='project_page'),
    url(r'^group_of_project/management/(?P<project_info_id>\d+)/$', 'project_info.views.show_project_management_page', name='project_management_page'),
)
