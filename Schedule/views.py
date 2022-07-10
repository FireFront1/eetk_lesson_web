import calendar
from datetime import datetime, timedelta, date

from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA
from django.db.models import Q
from django.shortcuts import render

from config.settings import USER_RANGE_START, USER_RANGE_END
from django import views

from .utils import filter_lessons

from .models import TimeTable, Teacher, Group, Cabinet


def main_page(request):
    teach = Teacher.objects.all().order_by('last_name')
    group = Group.objects.all().order_by('group_name')
    cabinet = Cabinet.objects.all().order_by('cabinet_name')
    search = request.GET.get('search')
    today = date.today()
    previous = today + relativedelta(weekday=MO(-2))
    current = today + relativedelta(weekday=MO(-1))
    next = today + relativedelta(weekday=MO(1))
    MondayP = previous + relativedelta(weekday=MO)
    MondayC = current + relativedelta(weekday=MO)
    MondayN = next + relativedelta(weekday=MO)
    TuesdayP = previous + relativedelta(weekday=TU)
    TuesdayC = current + relativedelta(weekday=TU)
    TuesdayN = next + relativedelta(weekday=TU)
    WednesdayP = previous + relativedelta(weekday=WE)
    WednesdayC = current + relativedelta(weekday=WE)
    WednesdayN = next + relativedelta(weekday=WE)
    ThursdayP = previous + relativedelta(weekday=TH)
    ThursdayC = current + relativedelta(weekday=TH)
    ThursdayN = next + relativedelta(weekday=TH)
    FridayP = previous + relativedelta(weekday=FR)
    FridayC = current + relativedelta(weekday=FR)
    FridayN = next + relativedelta(weekday=FR)
    SaturdayP = previous + relativedelta(weekday=SA)
    SaturdayC = current + relativedelta(weekday=SA)
    SaturdayN = next + relativedelta(weekday=SA)
    if search is not None:
        timetable = TimeTable.objects.filter(
            Q(teacher__first_name=search) | Q(teacher__last_name=search) |
            Q(teacher__middle_name=search) | Q(cabinet__cabinet_name=search) | Q(
                group__group_name__startswith=search
            ), date__range=[datetime.now() - timedelta(days=USER_RANGE_START),
                            datetime.now() + timedelta(days=USER_RANGE_END)]).order_by('-date')

        return render(request, 'lessons_list.html', {
            'search': search,
            'today': today,
            'previous': previous,
            'current': current,
            'next': next,
            'MondayP': MondayP,
            'TuesdayP': TuesdayP,
            'WednesdayP': WednesdayP,
            'ThursdayP': ThursdayP,
            'FridayP': FridayP,
            'SaturdayP': SaturdayP,
            'MondayC': MondayC,
            'TuesdayC': TuesdayC,
            'WednesdayC': WednesdayC,
            'ThursdayC': ThursdayC,
            'FridayC': FridayC,
            'SaturdayC': SaturdayC,
            'MondayN': MondayN,
            'TuesdayN': TuesdayN,
            'WednesdayN': WednesdayN,
            'ThursdayN': ThursdayN,
            'FridayN': FridayN,
            'SaturdayN': SaturdayN,
            'teacher_name': teach,
            'group_name': group,
            'cabinet_name': cabinet,
            'timetable': timetable})
    else:
        timetable = TimeTable.objects.filter(date__range=[datetime.now() - timedelta(days=datetime.now().weekday()),
                                                          datetime.now() + timedelta(
                                                              days=(6 - datetime.now().weekday()))]).order_by('-date')
        return render(request, 'lessons_list.html', {
            'teacher_name': teach,
            'group_name': group,
            'cabinet_name': cabinet,
            'timetable': timetable})


class LessonFilterView(views.generic.ListView):
    model = TimeTable
    template_name = 'lessons_list.html'

    def get_queryset(self):
        print(filter_lessons(self.request))
        return filter_lessons(self.request)
