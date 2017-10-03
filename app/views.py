from django.shortcuts import render, get_object_or_404 as get404
from django.http import (HttpResponse,
    HttpResponseForbidden, HttpResponseBadRequest,
    HttpResponseRedirect, Http404)
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives


from django.utils import timezone
from django.db import transaction

from datetime import timedelta, datetime

from .models import *

import textwrap

########### Create your views here.

def A(x):
    return '' + x

def find_student(name):
    res = None
    for x in Student.objects.all():
        if name.lower() in x.get_full_name().lower():
            if res:
                raise Http404('multiple student for name ' + name)
            res = x
    if res:
        return res
    else:
        raise Http404('student not found: ' + name)

def presence(request, session_search):
    if not request.user.is_staff:
        return HttpResponseForbidden('You must be <a href="/admin">admin</a>')
    
    if request.method == "GET":
        date = session_search.strip() if session_search.strip() else str(timezone.now().date())
        session = get404(Session, beg__startswith=date)
        
        return render(request, A('presence.html'), dict(
            session=session,
            students=session.group.student_set.all().order_by('first_name', 'last_name'),
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
    
    session = get404(Session, pk=R['session_pk'])
    
    with transaction.atomic():
        for student in students:
            session.presents.add(student)
    
    return HttpResponse('''
      <!DOCTYPE html>
      <html>
        <head><meta charset="utf-8" /> <meta name="viewport" content="width=device-width, initial-scale=1" /></head>
        <body>
        <p>Les {0} nouveaux présents ont été notés : {1}</p>
        <p><a href="/see/{2}">Voir la session du {2}</a></p>
        <p><a href="/mail/{2}">Envoyer un email pour la session du {2}</a></p>
        <p><a href="/feuille/">Voir la feuille</a></p>
        <p><a href="/admin">Admin</a></p>
        <p><a href="/admin/logout/">Se déconnecter</a></p>
        </body>
      </html>
        '''.format(
        len(students),
        ', '.join(sorted(x.get_full_name() for x in students)),
        str(session.beg.date()),
    ))

def see(request, date):
    if not request.user.is_staff:
        return HttpResponseForbidden('You must be <a href="/admin">admin</a>')
    
    date = date.strip() or str(timezone.now().date())
    try:
        session = Session.objects.get(beg__startswith=date)
    except Session.DoesNotExist:
        session = Session.objects.filter(beg__lt=date).order_by('-beg')[0]
    
    return render(request, A('session.html'), dict(
        session = session,
        presents = session.group.student_set.filter(session=session),
        absents = session.group.student_set.exclude(session=session),
        additionals = session.presents.exclude(group=session.group),
    ))

def mail(request, date):
    if not request.user.is_staff:
        return HttpResponseForbidden('You must be <a href="/admin">admin</a>')
    
    date = date.strip() or str(timezone.now().date())
    try:
        session = Session.objects.get(beg__startswith=date)
    except Session.DoesNotExist:
        session = Session.objects.filter(beg__lt=date).order_by('-beg')[0]
    
    presents = session.group.student_set.filter(session=session)
    absents = session.group.student_set.exclude(session=session)
    additionals = session.presents.exclude(group=session.group)
    
    head = 'Parascolaire Jeux Vidéos - Présences {} {:%d/%m/%Y}'.format(
        session.group.name,
        session.beg)
    
    msg = textwrap.dedent('''
    Bonjour, voici les présences du Parascolaire Jeux Vidéos.
    Groupe {} Séance {:%d/%m/%Y}.
    
    Absents ({}) :
    {}
    Présents ({}) :
    {}
    
    Élèves additionels ({}) :
    {}
    ''').strip().format(
        session.group.name,
        session.beg,
        absents.count(), "\n".join("  {} {}".format(x.last_name, x.first_name) for x in absents.order_by('last_name', 'first_name')),
        presents.count(), "\n".join("  {} {}".format(x.last_name, x.first_name) for x in presents.order_by('last_name', 'first_name')),
        additionals.count(), "\n".join("  {} {}".format(x.last_name, x.first_name) for x in additionals.order_by('last_name', 'first_name')))
    
    m = EmailMessage(head, msg, 'noreply@robertvandeneynde.be', ['vanessafulvo@hotmail.com'], cc=['robertvandeneynde@hotmail.com', 'meessen.thomas@gmail.com'], reply_to=['meessen.thomas@gmail.com'])
    m.send(fail_silently=False)
    
    return HttpResponse('Bien envoyé. Contenu : <pre>{}</pre>'.format(msg))

def feuille(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('You must be <a href="/admin">admin</a>')
    
    N = timezone.now()
    year = N.year if N.month >= 9 else N.year-1
    
    groups = list(Group.objects.filter(year=year).order_by('pk'))
    sessions = [group.session_set.order_by('beg') for group in groups]
    students = Student.objects.filter(group__year=year).order_by('group', 'first_name', 'last_name')
    
    infos = [
        [
            (student in session.presents.all(), session)
            for session in sessions[groups.index(student.group)]
        ]
        for student in students
    ]
    
    return render(request, A('feuille.html'), dict(
        session_list = list(zip(*sessions)),
        student_list = list(zip(students, infos)),
    ))
