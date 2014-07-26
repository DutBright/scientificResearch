# coding: UTF-8
'''
Created on 2014-06-07

Desc: school' view, includes home(manage), review report view
'''
from django.shortcuts import render
from django.db.models import Q

from common.views import scheduleManage, financialManage,researchConcludingManage
from teacher.forms import ProjectBudgetInformationForm,ProjectBudgetAnnualForm
from teacher.forms import SettingForm
from adminStaff.models import ProjectSingle, Re_Project_Expert
from users.models import ExpertProfile, SchoolProfile
from common.utils import status_confirm,APPLICATION_SCHOOL_CONFIRM
from backend.logging import loginfo
from school.forms import FilterForm
from backend.utility import getContext

def appView(request):
    context = {}
    return render(request,"school/application.html",context)
def scheduleView(request):

    userauth = {
                "role": "school",
                "status":"application"
    }
    return scheduleManage(request, userauth)

def judgeProjectView(request,pid,pass_p):
    project=ProjectSingle.objects.get(pk=pid)
    if pass_p=="1":
        status_confirm(project,APPLICATION_SCHOOL_CONFIRM)

    return scheduleView(request)

def financialView(request):
    userauth = {
                "role": 'school',                
    }
    return financialManage(request, userauth)


def financialInfoView(request):
    budgetinfoform = ProjectBudgetInformationForm()
    budgetannuform = ProjectBudgetAnnualForm()    
    context = {
        'budgetinfoform':budgetinfoform,
        'budgetannuform':budgetannuform,
    }
    return render(request,"school/project_financial_info.html",context)

def finalReportView(request):
    context = {}
    return render(request,"school/final.html",context)
def progressReportView(requset):
    context={}
    return render(requset,"school/progress.html",context)

def allocView(request):
    expert_list = ExpertProfile.objects.all()

    if request.method == "GET":
        project_list = ProjectSingle.objects.all()
        form = FilterForm(request = request)
    else:
        form = FilterForm(request.POST, request=request)
        if form.is_valid():
            college = form.cleaned_data["colleges"]
            special = form.cleaned_data["specials"]
            if college == "-1":
                project_list = ProjectSingle.objects.all()
            else:
                project_list = ProjectSingle.objects.filter(teacher__college = college)
            project_list = project_list.filter(project_special = special)
    for expert in expert_list:
        expert.alloc_num = Re_Project_Expert.objects.filter(Q(expert = expert) & Q(is_first_round = True)).count()
    
    context = getContext(project_list, 1, "item", 0)
    context.update({
                    "expert_list": expert_list,
                    "form": form,
                  })
    return render(request, "school/alloc.html", context)

def researchConcludingView(request):
    userauth={
        "role":"school",
        "status":"research_concluding",
    }
    return researchConcludingManage(request,userauth)

def finalAllocView(request):
    context = {}
    return render(request, "school/final_alloc.html", context)
def noticeMessageSettingView(request):
    context = {}
    return render(request, "school/notice.html", context)

def controlView(request):
    

    special = [     
              {
                'year_list': [2015,],
                'special_name': 'science',
    },
              {
                'year_list': [2011,2012,2013,2014,],
                'special_name': 'liberal',
    },
        
    ]


    
    context = {
        'special' :special,
    }
    return render(request, "school/control.html", context);

def infoModifyView(request):
    form = SettingForm()
    context = {"form": form,}
    return render(request, "school/teacher_info_modify.html", context)
