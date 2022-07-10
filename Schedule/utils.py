from datetime import datetime, timedelta

from Schedule.models import TimeTable
from django.db.models import Q

from config.settings import USER_RANGE_START, USER_RANGE_END


def filter_lessons(request):
    search = request.GET.get('search')
    start_date = request.GET.get("date_start")
    end_date = request.GET.get("date_end")
    if not request.user.is_superuser:
        start_date = ''
        end_date = ''
    if start_date == '' and end_date == '':
        if request.user.is_superuser:
            return TimeTable.objects.filter(
                Q(teacher__first_name=search) | Q(teacher__last_name=search) |
                Q(teacher__middle_name=search) | Q(cabinet__cabinet_name=search) | Q(
                    group__group_name__startswith=search
                )).order_by('-number').order_by('-date')
        else:
            return TimeTable.objects.filter(
                Q(teacher__first_name=search) | Q(teacher__last_name=search) |
                Q(teacher__middle_name=search) | Q(cabinet__cabinet_name=search) | Q(
                    group__group_name__startswith=search
                ), date__range=[datetime.now() - timedelta(days=USER_RANGE_START),
                                datetime.now() + timedelta(days=USER_RANGE_END)]).order_by('-date')
    if end_date == '':
        end_date = f'{datetime.now():%Y-%m-%d}'
        return TimeTable.objects.filter(
            Q(teacher__first_name=search) | Q(teacher__last_name=search) |
            Q(teacher__middle_name=search) | Q(cabinet__cabinet_name=search) |
            Q(date__range=[start_date, end_date]) | Q(
                group__group_name__startswith=search
            )).order_by('-number').order_by('-date')
    if start_date == '':
        return TimeTable.objects.filter(
            Q(teacher__first_name=search) | Q(teacher__last_name=search) |
            Q(teacher__middle_name=search) | Q(cabinet__cabinet_name=search) | Q(
                group__group_name__startswith=search
            )).order_by('-number').order_by('-date')
    else:
        if request.user.is_superuser:
            return TimeTable.objects.filter(
                Q(teacher__first_name=search) | Q(teacher__last_name=search) |
                Q(teacher__middle_name=search) | Q(cabinet__cabinet_name=search) |
                Q(date__range=[start_date, end_date]) | Q(
                    group__group_name__startswith=search
                )).order_by('-number').order_by('-date')
        else:
            return TimeTable.objects.filter(
                Q(teacher__first_name=search) | Q(teacher__last_name=search) |
                Q(teacher__middle_name=search) | Q(cabinet__cabinet_name=search) | Q(
                    group__group_name__startswith=search
                ), date__range=[datetime.now() - timedelta(days=USER_RANGE_START),
                                datetime.now() + timedelta(days=USER_RANGE_END)]).order_by('-number').order_by(
                '-date')