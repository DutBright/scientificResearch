# coding: UTF-8
from adminStaff.models import ProjectSingle
from backend.logging import loginfo
from django.db.models import Q
from const import *
from const.models import ProjectStatus

def get_application_year_choice():
    project_group=ProjectSingle.objects.all()
    year = [('-1',u"申请年度")]
    year_has=[]
    for item in project_group:
        year_has.append(item.application_year)
    year_has=list(set(year_has))
    
    for y in year_has:
        year.append((y,y))
    return tuple(year)
def get_approval_year_choice():
    project_group=ProjectSingle.objects.all()
    year = [('-1',u"立项年度")]
    year_has=[]
    for item in project_group:
        year_has.append(item.approval_year)
    year_has=list(set(year_has))
    for y in year_has:
        year.append((y,y))
    return tuple(year)
def get_status_choice():
    status_choice=[
        (PROJECT_STATUS_TASK_SCHOOL_OVER,u"任务书审核阶段"),
        (PROJECT_STATUS_PROGRESS_SCHOOL_OVER,u"进展报告审核阶段"),
        (PROJECT_STATUS_FINAL_REVIEW_OVER,u"结题书审核阶段"),
        (PROJECT_STATUS_OVER,u"结题")
    ]
    return status_choice
def get_application_status_choice():
    application_status_choice=[
        (PROJECT_STATUS_APPLY,u"网上申请未提交"),
        (PROJECT_STATUS_APPLICATION_WEB_OVER,u"申报书未提交"),
        (PROJECT_STATUS_APPLICATION_COMMIT_OVER,u"待审核"),
        (PROJECT_STATUS_APPLICATION_COLLEGE_OVER,u"院级审核完成"),
        (PROJECT_STATUS_APPLICATION_EXPERT_SUBJECT,u"专题审核完成"),
    ]
    return application_status_choice
def get_query_status(status):
    status=int(status)
    if status==PROJECT_STATUS_TASK_SCHOOL_OVER:
        return (PROJECT_STATUS_APPROVAL,status)
    elif status==PROJECT_STATUS_PROGRESS_SCHOOL_OVER:
        return (PROJECT_STATUS_TASK_SCHOOL_OVER,status)
    elif status==PROJECT_STATUS_FINAL_REVIEW_OVER:
        return (PROJECT_STATUS_PROGRESS_SCHOOL_OVER,status)
    else:
        return (status,status)
def get_query_application_status(status):
    status=int(status)
    if status==PROJECT_STATUS_APPLY:
        return (status,status)
    elif status==PROJECT_STATUS_APPLICATION_WEB_OVER:
        return (0,status)
    elif status==PROJECT_STATUS_APPLICATION_COMMIT_OVER:
        return (status,status)
    elif status==PROJECT_STATUS_APPLICATION_COLLEGE_OVER:
        return (status,status)
    else:
        return (PROJECT_STATUS_APPLICATION_SCHOOL_OVER,status)

def create_QE(status):
    return Q(project_status__status=status)
def create_Q(start,end):

    return Q(project_status__status__gte=start,project_status__status__lte=end)

def get_qset(userauth):
    if userauth['role']=="school" :
        if userauth['status']=="application":
            pending=create_QE(PROJECT_STATUS_APPLICATION_COLLEGE_OVER)
            default=create_QE(PROJECT_STATUS_APPLICATION_SCHOOL_OVER)
            search=create_Q(PROJECT_STATUS_APPLY,PROJECT_STATUS_APPLICATION_EXPERT_SUBJECT)
        else:
            pending=create_QE(PROJECT_STATUS_TASK_COMMIT_OVER)|create_QE(PROJECT_STATUS_PROGRESS_COMMIT_OVER)|create_QE(PROJECT_STATUS_FINAL_COMMIT_OVER)
            default=create_QE(PROJECT_STATUS_TASK_SCHOOL_OVER)|create_QE(PROJECT_STATUS_PROGRESS_SCHOOL_OVER)|create_QE(PROJECT_STATUS_FINAL_SCHOOL_OVER)
            search=create_Q(PROJECT_STATUS_APPROVAL,PROJECT_STATUS_OVER)
    elif userauth['role']=="college":
        if userauth['status']=="application":
            pending=create_QE(PROJECT_STATUS_APPLICATION_COMMIT_OVER)
            default=create_QE(PROJECT_STATUS_APPLICATION_COLLEGE_OVER)
            search=create_Q(PROJECT_STATUS_APPLY,PROJECT_STATUS_APPLICATION_EXPERT_SUBJECT)
        else:
            pending=Q()
            default=create_QE(PROJECT_STATUS_TASK_SCHOOL_OVER)|create_QE(PROJECT_STATUS_PROGRESS_SCHOOL_OVER)|create_QE(PROJECT_STATUS_FINAL_SCHOOL_OVER)
            search=create_Q(PROJECT_STATUS_APPROVAL,PROJECT_STATUS_OVER)
    else:
        if userauth['status']=="budget":
            pending=create_QE(PROJECT_STATUS_TASK_COMMIT_OVER)
            default=create_QE(PROJECT_STATUS_TASK_FINANCE_OVER)
            search=create_Q(PROJECT_STATUS_APPROVAL,PROJECT_STATUS_OVER)
        else:
            pending=create_QE(PROJECT_STATUS_FINAL_COMMIT_OVER)
            default=create_QE(PROJECT_STATUS_FINAL_FINANCE_OVER)
            search=create_Q(PROJECT_STATUS_APPROVAL,PROJECT_STATUS_OVER)
    return (pending,default,search)

def statusRollBack(project,userrole,userstatus,form):
    project.project_sendback_status=project.project_status
    if userrole=="school":
        if userstatus=="application":
            form_list=form.getlist("application")
            if len(form_list)==2:
               
                set_status(project,PROJECT_STATUS_APPLY)
                project.file_application=False
                project.save()
            elif len(form_list)==1:
                if form_list[0]=="网上提交不合格":
                    set_status(project,PROJECT_STATUS_APPLY)
                elif form_list[0]=="申报书不合格":
                    set_status(project,PROJECT_STATUS_APPLICATION_WEB_OVER)
                    project.file_application=False
                    project.save()
                else:
                    return False 
            else:
                return False
        elif userstatus=="research_concluding":
            if project.project_status.status==PROJECT_STATUS_TASK_FINANCE_OVER:
                set_status(project,PROJECT_STATUS_TASK_BUDGET_OVER)
                project.file_task=False
                project.save()
            elif project.project_status.status==PROJECT_STATUS_PROGRESS_COMMIT_OVER:
                set_status(project,PROJECT_STATUS_SCHOOL_OVER)
                project.file_interimachecklist=False
                project.save()
            elif project.project_status.status==PROJECT_STATUS_FINAL_FINANCE_OVER:
                form_list=form.getlist("final")
                if len(form_list)==2:
                    set_status(project,PROJECT_STATUS_PROGRESS_SCHOOL_OVER)
                    project.file_task=False
                    project.save()
                elif len(form_list==1):
                    if form_list[0]=="网上提交不合格":
                        set_status(project,PROJECT_STATUS_PROGRESS_SCHOOL_OVER)
                    elif form_list[1]=="结题书不合格":
                        set_status(project,PROJECT_STATUS_FINAL_WEB_OVER)
                        project.file_summary=False;
                        project.save()
                    else:
                        return False
                else:
                    return False
            else :
                return False
        else:
            return False
    elif userrole=="college":
        form_list=form.getlist("application")
        if len(form_list)==2:
            set_status(project,PROJECT_STATUS_APPLY)
            project.file_application=False
            project.save()
        elif len(form_list)==1:
            if form_list[0]=="网上提交不合格":
                set_status(project,PROJECT_STATUS_APPLY)
            elif form_list[0]=="申报书不合格":
                set_status(project,PROJECT_STATUS_APPLICATION_WEB_OVER)
                project.file_application=False
                project.save()
            else:
                return False 
        else:
            return False
    elif userrole=="finance":
        if userstatus=="budget":
            set_status(project,PROJECT_STATUS_APPROVAL)
        elif userstatus=="final":
            set_status(project,PROJECT_STATUS_PROGRESS_SCHOOL_OVER)
        else:
            return False
    else:
        return False
    project.save()
    return True



def set_status(project,status):
    project.project_status=ProjectStatus.objects.get(status=status)
    project.save()
def status_confirm(project, confirm):
    if confirm==-1:
        set_status(project,project.project_status.status+1)
        if project.project_status.status==project.project_sendback_status.status:
            set_status(project,project.project_status.status+1)
    return True
    if project.project_status.status==PROJECT_STATUS_APPLY:
        if confirm==APPLICATION_WEB_CONFIRM:
            if project.file_application==True:
                set_status(project,PROJECT_STATUS_APPLICATION_COMMIT_OVER)
            else:
                set_status(project,PROJECT_STATUS_APPLICATION_WEB_OVER)
        elif confirm==APPLICATION_SUBMIT_CONFIRM:
            pass
        else:
            return False

    elif project.project_status.status==PROJECT_STATUS_APPLICATION_WEB_OVER:
        if confirm==APPLICATION_SUBMIT_CONFIRM:
            set_status(project,PROJECT_STATUS_APPLICATION_COMMIT_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_APPLICATION_COMMIT_OVER:
        if confirm==APPLICATION_COLLEGE_COMFIRM:
            set_status(project,PROJECT_STATUS_APPLICATION_COLLEGE_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_APPLICATION_COLLEGE_OVER:
        if confirm==APPLICATION_SCHOOL_CONFIRM:
            set_status(project,PROJECT_STATUS_APPLICATION_SCHOOL_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_APPLICATION_SCHOOL_OVER:
        if confirm==APPLICATION_EXPERT_SUBJECT_CONFIRM:
            set_status(project,PROJECT_STATUS_APPLICATION_EXPERT_SUBJECT)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_APPLICATION_EXPERT_SUBJECT:
        if confirm==APPLICATION_REVIEW_CONFIRM:
            set_status(project,PROJECT_STATUS_APPLICATION_REVIEW_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_APPLICATION_REVIEW_OVER:
        if confirm==APPROVAL_CONFIRM:
            set_status(project,PROJECT_STATUS_APPROVAL)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_APPROVAL:
        if confirm==TASK_BUDGET_CONFIRM:
            if project.file_task==True:
                set_status(project,PROJECT_STATUS_TASK_COMMIT_OVER)
            else:
                set_status(project,PROJECT_STATUS_TASK_BUDGET_OVER)
        elif confirm==TASK_SUBMIT_CONFIRM:
            pass
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_TASK_BUDGET_OVER:
        if confirm==TASK_SUBMIT_CONFIRM:
            set_status(project,PROJECT_STATUS_TASK_COMMIT_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_TASK_COMMIT_OVER:
        if confirm==TASK_FINANCE_CONFIRM:
            set_status(project,PROJECT_STATUS_TASK_FINANCE_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_TASK_FINANCE_OVER:
        if confirm==TASK_SCHOOL_CONFIRM:
            set_status(project,PROJECT_STATUS_SCHOOL_OVER)
        else:
            return False        
    
    elif project.project_status.status==PROJECT_STATUS_SCHOOL_OVER:
        if confirm==PROGRESS_SUBMIT_CONFIRM:
            set_status(project,PROJECT_STATUS_PROGRESS_COMMIT_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_PROGRESS_COMMIT_OVER:
        if confirm==PROGRESS_SCHOOL_CONFIRM:
            set_status(project,PROJECT_STATUS_PROGRESS_SCHOOL_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_PROGRESS_SCHOOL_OVER:
        if confirm==FINAL_WEB_CONFIRM:
            if project.file_summary==TRUE:
                set_status(project,PROJECT_STATUS_FINAL_COMMIT_OVER)
            else:
                set_status(project,PROJECT_STATUS_FINAL_WEB_OVER)
        elif confirm==FINAL_SUBMIT_CONFIRM:
            pass
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_FINAL_WEB_OVER:
        if confirm==FINAL_SUBMIT_CONFIRM:
                set_status(project,PROJECT_STATUS_FINAL_COMMIT_OVER)
        else :
            return False
    elif project.project_status.status==PROJECT_STATUS_FINAL_COMMIT_OVER:
        if confirm==FINAL_FINANCE_CONFIRM:
            set_status(project,PROJECT_STATUS_FINAL_FINANCE_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_FINAL_FINANCE_OVER:
        if confirm==FINAL_SCHOOL_CONFIRM:
            set_status(project,PROJECT_STATUS_FINAL_SCHOOL_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_FINAL_SCHOOL_OVER:
        if confirm==FINAL_EXPERT_SUBJECT_CONFIRM:
            set_status(project,PROJECT_STATUS_FINAL_EXPERT_SUBJECT)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_FINAL_EXPERT_SUBJECT:
        if confirm==PROJECT_OVER_CONFIRM:
            set_status(project,PROJECT_STATUS_FINAL_REVIEW_OVER)
        else:
            return False
    elif project.project_status.status==PROJECT_STATUS_FINAL_REVIEW_OVER:
        if confirm==PROJECT_OVER_CONFIRM:
            set_status(project,PROJECT_STATUS_OVER)
        else:
            return False
    else:
        return False
    return True

        
