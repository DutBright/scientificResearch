# coding: UTF-8
'''
Created on 2013-3-29

@author: sytmac
'''
import os, sys,pickle
from django.shortcuts import get_object_or_404
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.template.loader import render_to_string

#from adminStaff.forms import NumLimitForm, TimeSettingForm, SubjectCategoryForm, ExpertDispatchForm,SchoolDispatchForm,TemplateNoticeForm,FundsChangeForm,StudentNameForm, SchoolDictDispatchForm

from django.db.models import Q
from backend.logging import loginfo
from const import *
from adminStaff.models import ProjectSingle
from common.utils import status_confirm
from const import *
OVER_STATUS_NOTOVER = "notover"
OVER_STATUS_OPENCHECK = "opencheck"
OVER_STATUS_MIDCHECK = "midcheck"
OVER_STATUS_FINCHECK = "fincheck"
OVER_STATUS_NORMAL = "normal"

OVER_STATUS_CHOICES = (
    ('no', u"未结题"),
    ('yes', u"已结题"),    
)
@dajaxice_register
def getStatus(request):
    return simplejson.dumps({
        "application_c":PROJECT_STATUS_APPLICATION_COMMIT_OVER,
        "application_s":PROJECT_STATUS_APPLICATION_COLLEGE_OVER,
        "final":PROJECT_STATUS_FINAL_COMMIT_OVER,
    })
@dajaxice_register
def LookThroughResult(request,judgeid,userrole,userstatus,look_through_form):
    project=ProjectSingle.objects.get(pk=judgeid)
    form=deserialize_form(look_through_form)
    if form["judgeresult"]=="1":
        status_confirm(project,-1)
    else:
    
        comment={
            "Judger":request.user.last_name,
            "Article":form.getlist('application').extend(form.getlist("final")),
            "description":form["reason"]
        }
        project.comment=eval(comment)
        project.save()
        statusRollBack(project,userrole,userstatus,form)
    context=schedule_form_data(request,{
        "role":userrole,
        "status":userstatus
    })
    if userstatus=="application":
        table_html=render_to_string("widgets/project_filter.html",context)
    else:
        table_html=render_to_string("widgets/research_concluding_table.html",context)
    return simplejson.dumps({"table_html":table_html})   
@dajaxice_register
def change_project_overstatus(request, project_id, changed_overstatus):
    '''
    change project overstatus
    '''
    choices = dict(OVER_STATUS_CHOICES)


    res = choices[changed_overstatus]    
    return simplejson.dumps({'status':'1', 'res':res})

    if changed_overstatus in choices:
        AdminStaffService.ProjectOverStatusChange(project_id, changed_overstatus)
        res = choices[changed_overstatus]
    else:
        res = "操作失败，请重试"
    return simplejson.dumps({'status':'1', 'res':res})
