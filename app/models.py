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
    
    def __str__(self):
        return self.get_full_name()
    
class Session(Model):
    group = FK(Group)
    beg = DateTimeField()
    end = DateTimeField()
    
    presents = ManyToManyField(Student, blank=True)
    
    def __str__(self):
        return "{} {}".format(self.group, self.beg.date())
    
