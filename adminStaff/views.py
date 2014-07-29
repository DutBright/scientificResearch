# coding: UTF-8
'''
Created on 2014-06-07

Desc: adminStaff' view, includes home(manage), review report view
'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators import csrf
from backend.decorators import *
from const import *
from backend.logging import loginfo
from backend.utility import getContext

from adminStaff.forms import NewsForm,ObjectForm,TemplateNoticeMessageForm,DispatchForm,DispatchAddCollegeForm
from teacher.forms import ProjectBudgetInformationForm,ProjectBudgetAnnualForm, SettingForm
from common.forms import NoticeForm

from common.views import scheduleManage, financialManage,noticeMessageSettingBase,scheduleManage

from adminStaff.models import TemplateNoticeMessage,News
from users.models import SchoolProfile,CollegeProfile,ExpertProfile,Special,College

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def appView(request):

    context = {}
    return render(request, "adminStaff/application.html", context)

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def allocManageView(request):
    userauth = {
        'role': 'adminStaff',
    }
    object_form = ObjectForm()

    #special
    special_list = []
    user_special_info = {}
    for i in Special.objects.all() :
        special_list.append({'name':i.name, 'user':i.school_user, })

    for i in SchoolProfile.objects.all():
        user_special_info[i] = []   
    
    for i in special_list:
        if i['user']:
            user_special_info[i['user']].append(i['name'])
    # college
    college_list = []
    user_college_info = {}
    for i in College.objects.all() :
        college_list.append({'name':i.name, 'user':i.college_user, })
    for i in CollegeProfile.objects.all():
        user_college_info[i] = []   
    for i in college_list:
        if i['user']:
            user_college_info[i['user']].append(i['name'])
    instance_list = [ 
        {
            'object_chinese_name':"专题",
            'object_name': "special",
            'object_form': object_form,
            'object_list': special_list,
            'user_object_info':user_special_info,
        },
        {
            'object_chinese_name':"学院",
            'object_name': "college",
            'object_form': object_form,
            'object_list': college_list,
            'user_object_info':user_college_info,
        },
    ]
    context = { 
    'instance_list': instance_list,
    }

    return render(request, "adminStaff/alloc_manage.html", context)

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def scheduleView(request):


    userauth = {
        'role': 'adminStaff',
        'status':'application'
    }
    return scheduleManage(request, userauth)

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def newsRelease(request):
    if request.method == "GET":
        form = NewsForm()
    else:
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    newsList = News.objects.all()
    context={"newsform":NewsForm,
             "newsList":newsList}
    return render(request,"adminStaff/news_release.html",context)

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def noticeMessageSetting(request):
    userauth={
        "role":"adminStaff"
    }
    return noticeMessageSettingBase(request,userauth)
def dispatchView(request):
    dispatch_form = DispatchForm()
    dispatchAddCollege_form=DispatchAddCollegeForm()
    college_users = CollegeProfile.objects.all()
    expert_users = ExpertProfile.objects.all()
    school_users = SchoolProfile.objects.all()
    loginfo(college_users.count())
    loginfo(school_users.count())
    context = {
               "dispatch_form":dispatch_form,
               "dispatchAddCollege_form":dispatchAddCollege_form,
               "college_users":college_users,
               "school_users":school_users,
               "users":expert_users,
    }
    return render(request, "adminStaff/dispatch.html", context)

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def financialView(request):
    userauth = {
                "role": 'adminStaff', 
    }
    return financialManage(request, userauth)


@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def financialInfoView(request):
    budgetinfoform = ProjectBudgetInformationForm()
    budgetannuform = ProjectBudgetAnnualForm()    
    context = {
        'budgetinfoform':budgetinfoform,
        'budgetannuform':budgetannuform,
    }
    return render(request,"adminStaff/project_financial_info.html",context)

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def infoModifyView(request):
    context = {}
    return render(request, "adminStaff/teacher_info_modify.html", context)

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def infoExportView(request):
    context = {}
    return render(request, "adminStaff/infoexport.html", context)
