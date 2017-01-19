from django.shortcuts import render, get_object_or_404 as get404
from django.http import (HttpResponse,
    HttpResponseForbidden, HttpResponseBadRequest,
    HttpResponseRedirect, Http404)

from django.utils import timezone
from django.db import transaction

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
    if not request.user.is_staff:
        return HttpResponseForbidden('You must be admin')
    
    if request.method == "GET":
        date = request.GET.get('date', timezone.now().date()) # or datetime, anyway string
        session = get404(Session, beg__startswith=date)
        
        return render(request, A('presence.html'), dict(
            group=session.group,
            students=session.group.student_set.all().order_by('first_name', 'last_name'),
            date=date,
            # name_of_group='Lundi',
            # students=[Student(first_name='marco', pk=2), Student(first_name='polo', pk=7)],
        ))
    
    assert request.method == "POST"
    
    R = request.POST
    
    names = [name for name in R.getlist('name') if name]
    
    try:
        students = set(
            find_student(name) if not name.isdigit() else
            get404(Student, pk=name)
            for name in names)
    except Http404 as e:
        return HttpResponseBadRequest(str(e))
    
    if not students:
        return HttpResponseBadRequest('must be at least one student')
    
    date = R.get('date', timezone.now().date()) # or datetime, anyway string
    session = get404(Session, beg__startswith=date)
    
    with transaction.atomic():
        for student in students:
            session.presents.add(student)
    
    # exclude Students student where student is_present session
    absents = session.group.student_set.exclude(session=session)
    presents = session.group.student_set.filter(session=session)
    
    return HttpResponse('''
        <p>Les {} nouveaux présents ont été notés : {}</p>
        <h1>Résumé de la session {}</h1>
        <h2>Il y a {} absent(s) :</h2>
        <ol>{}</ol>
        <h2>Parmi les {} présent(s) :</h2>
        <ol>{}</ol>
        '''.format(
        len(students),
        ', '.join(sorted(x.get_full_name() for x in students)),
        session,
        absents.count(),
        ''.join(map("<li>{}</li>".format, sorted(x.get_full_name() for x in absents))),
        presents.count(),
        ''.join(map("<li>{}</li>".format, sorted(x.get_full_name() for x in presents))),
    ))

def see(request, date):
    if not request.user.is_staff:
        return HttpResponseForbidden('You must be admin')
    
    date = date.strip() or timezone.now().date()
    try:
        session = Session.objects.get(beg__startswith=date)
    except Session.DoesNotExist:
        session = Session.objects.filter(beg__lt=date).order_by('-beg')[0]
    
    return render(request, A('see_session.html'), dict(
        session = session,
        presents = session.group.student_set.filter(session=session),
        absents = session.group.student_set.exclude(session=session),
        additionals = session.presents.exclude(group=session.group),
    ))

def feuille(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('You must be admin')
    
    groups = list(Group.objects.order_by('pk'))
    sessions = [group.session_set.order_by('beg') for group in groups]
    students = Student.objects.all().order_by('group', 'first_name', 'last_name')
    
    infos = [
        [
            (student in session.presents.all(), session)
            for session in sessions[groups.index(student.group)]
        ]
        for student in students
    ]
    
    return render(request, A('see_feuille.html'), dict(
        session_list = list(zip(*sessions)),
        student_list = list(zip(students, infos)),
    ))