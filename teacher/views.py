# coding: UTF-8
'''
Created on 2014-06-07

Desc: teacher' view, includes home(manage), review report view
'''
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from const import * 
from teacher.forms import ProjectBudgetInformationForm,ProjectBudgetAnnualForm, SettingForm
from common.views import scheduleManage,finalReportViewWork
from common.forms import ProjectInfoForm, BasisContentForm, BaseConditionForm

def appView(request):

    project_info_form = ProjectInfoForm()
    basis_content_form = BasisContentForm()
    base_condition_form = BaseConditionForm()
    context = {
        'project_info_form': project_info_form,
        'basis_content_form':basis_content_form,
        'base_condition_form':base_condition_form,

    }
    return render(request,"teacher/application.html",context)
    
def homeView(request):
    context = {

    }
    return render(request,"teacher/project_info.html",context)
def memberChange(request):
    professional=PROFESSIONAL_TITLE
    executive=EXECUTIVE_POSITION
    context={}
    context['professional']=professional
    context['executive']=executive
    return render(request,"teacher/member_change.html",context)

def commitmentView(request):
    context = {}
    return render(request, "teacher/commitment.html", context)

def finalReportView(request):

    context = finalReportViewWork(request)
    if context['redirect']:
		return HttpResponseRedirect('/teacher/finalinfo')
    return render(request,"teacher/final.html",context)

def progressReportView(request):
    context = {}
    return render(request,"teacher/progress.html",context)

def fileView(request):
    data={};
    return render(request,"teacher/file_upload.html",data)

def settingView(request):
    form = SettingForm()
    context = {"form": form}
    return render(request, "teacher/setting.html", context)

def financialView(request):
    if request.method == "POST":
        budgetinfoform = ProjectBudgetInformationForm(request.POST)
        budgetannuform = ProjectBudgetAnnualForm(request.POST)
        if budgetinfoform.is_valid():
            budgetinfo = budgetinfoform.cleaned_data
            print budgetinfo['project_basicexpenses']
    else:
        budgetinfoform = ProjectBudgetInformationForm()
        budgetannuform = ProjectBudgetAnnualForm()

    context = {
        'budgetinfoform':budgetinfoform,
        'budgetannuform':budgetannuform,
    }
    return render(request,"teacher/financial.html",context)

def finalInfoView(request):

    context = {

    }
    return render(request,"teacher/finalinfo.html",context)
