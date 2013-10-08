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
    url(r'^$', 'user_status.views.show_root'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login_page'),
    url(r'^logout/$', 'user_status.views.logout_user', name='logout_page'),
    url(r'^create_group_page/$', 'group_info.views.create_group', name='create_group_page'),
)
