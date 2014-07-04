'''
Created on 2013-3-18

@author: sytmac
'''
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from teacher import views as teacher_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = patterns('',
    url(
        r'^$',
        teacher_views.homeView,
       ),
    url(
        r'^memberchange$',
        teacher_views.memberChange,
       ),
    url(
        r'^application$',
        teacher_views.appView,
       ),
    url(
        r'final$',
        teacher_views.finalReportView,
	),
    url(
        r'commitment',
        teacher_views.commitmentView,
    ),
    url(
        r'setting$',
        teacher_views.settingView,
    ),
	url(
		r'financial$',
		teacher_views.financialView,
	),
    url(
        r'progress$',
        teacher_views.progressReportView,
    ),
    url(
        r'file_upload$',
        teacher_views.fileView,
    ),
    url(
        r'finalinfo$',
        teacher_views.finalInfoView,
    ),
)
urlpatterns += staticfiles_urlpatterns()
