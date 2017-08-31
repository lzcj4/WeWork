from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
from django.urls import reverse
from django.views import generic
import datetime

from .models import *


# Create your views here.

def index(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    persons = Person.objects.all()
    context["persons"] = persons

    if request.method in ["POST"]:
        monday = str_to_date(request.POST.get("start_date", timezone.datetime.now().date().strftime("%Y-%m-%d")))
        next_monday = str_to_date(request.POST.get("end_date", timezone.datetime.now().date().strftime("%Y-%m-%d")))
        context["end_date"] = get_local_date(next_monday)
    elif request.method in ["GET"]:
        today = datetime.date.today()
        weekday = today.weekday()
        delta_day = datetime.timedelta(weekday)
        monday = today - delta_day
        sunday = today + datetime.timedelta(7 - weekday - 1)
        next_monday = today + datetime.timedelta(7 - weekday)
        context["end_date"] = get_local_date(sunday)

    context["start_date"] = get_local_date(monday)
    records = {}
    for p in persons:
        wr_set = p.workrecord_set.filter(p_work_date__gte=monday, p_work_date__lte=next_monday)
        if not records.get(p.p_name):
            records[p.p_name] = {}
        for r in wr_set:
            records[p.p_name][r.project.p_name] = records[p.p_name].get(r.project.p_name, 0) + r.p_hours

    context["records"] = records
    # context["title"] = "<script>alert('Wework <b> InfoSys')</script>"
    # context["title"] = "We-work InfoSys"
    return render(request, 'manday/index.html', context)


class PersonDetail(generic.ListView):
    model = WorkRecord
    template_name = 'manday/persondetail.html'
    context_object_name = 'recorder_list'

    def get_queryset(self):
        return WorkRecord.objects.filter(person_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super(PersonDetail, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.get_queryset()
        return context


def person_detail(request, person_id):
    list = WorkRecord.objects.filter(person_id=person_id)
    return render(request, 'manday/persondetail.html', {"recorder_list": list})


def manday_add(request, person_id):
    if request.method in ["POST"]:
        project_id = int(request.POST.get("project_id", ""))
        hours = float(request.POST.get("hours", ""))
        work_date = str_to_date(request.POST.get("p_work_date", ""))
        input_date = timezone.datetime.strptime(
            "{0} {1}".format(request.POST.get("p_input_date", timezone.datetime.now().date().strftime("%Y-%m-%d")),
                             request.POST.get("p_input_time", timezone.datetime.now().time().strftime("%H:%M:%S"))),
            "%Y-%m-%d %H:%M:%S")
        person = get_object_or_404(Person, id=person_id)
        row = person.workrecord_set.create(project_id=project_id, p_hours=hours, p_work_date=work_date,
                                           p_add_time=input_date)
        return HttpResponseRedirect(reverse('manday:index'))
    else:
        projects = Project.objects.all()
        return render(request, 'manday/add.html', {"projects": projects})


def manday_delete(request, manday_id):
    # get_object_or_404(WorkRecord, person_id=person_id)
    item = get_object_or_404(WorkRecord, id=manday_id)
    item.delete()
    return HttpResponseRedirect(reverse('manday:person_detail', args=(item.person.id,)))


@register.simple_tag
def get_item(dictionary, person_name, project_name):
    p_dic = dictionary.get(person_name)
    result = 0
    if p_dic:
        result = p_dic.get(project_name, 0)
    return result


@register.filter
def get_total(dictionary, person_name):
    """
    时间总计
    :param dictionary:人员字典
    :param person_name:人员名
    :return:总时长
    """
    p_dic = dictionary.get(person_name)
    result = 0
    if p_dic:
        result = sum((item for item in p_dic.values()))
    return result


@register.filter
def get_local_date(dt):
    return dt.strftime("%Y-%m-%d")


@register.filter
def get_local_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def str_to_date(date_str):
    return timezone.datetime.strptime(date_str.strip(), "%Y-%m-%d")