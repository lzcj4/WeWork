from django.db import models
from django.utils import timezone


# Create your models here.

class Person(models.Model):
    p_name = models.CharField(max_length=20, verbose_name="姓名")
    p_no = models.CharField(max_length=20, verbose_name="工号")
    p_dep = models.CharField(max_length=50, verbose_name="部门")
    p_in_date = models.DateField(verbose_name="入职时间")

    class Meta:
        index_together = ["p_name"]

    def __str__(self):
        return "{0}:{1}".format(self.p_no, self.p_name)


class Project(models.Model):
    p_name = models.CharField(max_length=50, verbose_name="项目名")
    p_launch_date = models.DateField(verbose_name="启动时间")

    def __str__(self):
        return "{0}".format(self.p_name)


class WorkRecord(models.Model):
    person = models.ForeignKey(Person, verbose_name="人员")
    project = models.ForeignKey(Project, verbose_name="项目名")
    p_hours = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="时长")
    p_work_date = models.DateField(verbose_name="工作日")
    p_add_time = models.DateTimeField(verbose_name="录入时间")
    p_comment = models.CharField(max_length=400, verbose_name="备注", default="")

    def __str__(self):
        return "{0},{1},{2}".format(self.person.p_name, self.project.p_name, self.p_hours)
