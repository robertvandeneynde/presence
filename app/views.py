from django.shortcuts import render, get_object_or_404 as get404
from django.http import (HttpResponse,
    HttpResponseForbidden, HttpResponseBadRequest,
    HttpResponseRedirect, Http404)

from django.utils import timezone

from datetime import timedelta, datetime

from .models import *

# Create your views here.

def A(x):
    return '' + x

def find_student(name):
    for x in Student.objects.all():
        if name.lower() in x.get_full_name().lower():
            return x
    raise Http404('student not found: ' + name)

def presence(request):
    #if not request.user.is_staff:
    #    return HttpResponseForbidden('You must be admin')
    
    if request.method != "POST":
        # session = get404(Session, beg__startswith=timezone.now().date())
        
        return render(request, A('presence.html'), dict(
            # name_of_group=session.group.name,
            # students=session.group.student_set.all().order_by('first_name', 'last_name')))
            name_of_group='Lundi',
            students=[Student(first_name='marco', pk=2), Student(first_name='polo', pk=7)],
        ))
    
    R = request.POST
    
    names = [name for name in R.getlist('name') if name]
    return HttpResponse(', '.join(names))
    
    students = set(
        find_student(name) if not name.isdigit() else
        get404(Student, pk=name)
        for name in names)
    
    if not students:
        return HttpResponseBadRequest('must be at least one student')
    
    date = R.get('date', timezone.now().date()) # or datetime, anyway string
    session = get404(Session, beg__startswith=date)
    
    for student in students:
        Presence.objects.create(student=student, session=session)
    
    absents = set(
        s for s in Student.objects.filter(normal_group=session.group)
        if s not in students)
    
    return HttpResponse('Created {} presences : <br/> {}, <br/> therefore {} absents : <br/>{}<br/>'.format(
        len(students),
        '<br />'.join(sorted(students, key=lambda x:x.get_full_name())),
        len(absents),
        '<br />'.join(sorted(absents, key=lambda x:x.get_full_name()))))
