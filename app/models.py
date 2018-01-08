from django.db import models 
from django.db.models import (Model,
    DateTimeField, IntegerField, ForeignKey,
    CharField, ManyToManyField)
from django.contrib.auth.models import User

def FK(cls):
    return ForeignKey(cls, on_delete=models.PROTECT)

class Group(Model):
    day = IntegerField() # 0 = monday
    year = IntegerField()
    name = CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Student(User):
    group = FK(Group)
    classe = CharField(max_length=10)
    
    other_year = ManyToManyField('self', symmetrical=True, blank=True) # link to same student over all years (ie. if a student has been there 3 years, each Student object will have 2 other_year students, the 3 Student form a clique of the Student.other_year graph
    
    def __str__(self):
        return self.get_full_name()
    
class Session(Model):
    group = FK(Group)
    beg = DateTimeField()
    end = DateTimeField()
    
    presents = ManyToManyField(Student, blank=True) # blank such that when adding a Sesssion in the admin, one can write "0 presents"
    
    def __str__(self):
        return "{} {}".format(self.group, self.beg.date())

