from django.contrib import admin

from django.db.models import get_models, get_app
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import *

def add(cls, *disp):
    class Admin(admin.ModelAdmin):
        list_display = disp # tuple(cls._meta.get_all_field_names())

    admin.site.register(cls, Admin)

add(Group, 'year', 'name')
add(Session, 'group', 'beg', 'end')
add(Student, 'first_name', 'last_name', 'group', 'classe')
# add(Presence, 'student', 'session')