# coding: UTF-8
'''
Created on 2013-04-02

@author:

Desc: Registration and login redirect
'''

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from registration.models import RegistrationProfile
from backend.decorators import check_auth
from const import *


def active(request, activation_key,
           template_name='registration/activate.html',
           extra_context=None):
    """
    Active the user account from an activation key.
    """
    activation_key = activation_key.lower()
    account = RegistrationProfile.objects.activate_user(activation_key)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'account': account,
                               'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS
                               },
                              context_instance=context)

def login_redirect(request):
    """
    When the user login, it will decide to jump the according page, in other
    words, school user will be imported /school/ page, if the user have many
    authorities, the system will jump randomly
    """
    #TODO: I will use reverse function to redirect, like school and expert
    if check_auth(request.user, SCHOOL_USER):
        return HttpResponseRedirect(reverse('school.views.home_view'))
    elif check_auth(request.user, EXPERT_USER):
        return HttpResponseRedirect(reverse('expert.views.home_view'))
    elif check_auth(request.user, ADMINSTAFF_USER):
        return HttpResponseRedirect('/adminStaff/')
    elif check_auth(request.user, STUDENT_USER):
        return HttpResponseRedirect('/student/')
    elif check_auth(request.user, TEACHER_USER):
        return HttpResponseRedirect('/teacher/')
    else:
        return HttpResponseRedirect('/')
