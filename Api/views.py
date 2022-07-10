from datetime import timedelta, datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from Schedule.models import TimeTable, Cabinet, Teacher, Group


class GetLessons(APIView):
    @staticmethod
    def get(request):
        list_lessons = []
        queryset = TimeTable.objects.filter(date__range=[datetime.now() - timedelta(days=datetime.now().weekday()),
                                                         datetime.now() + timedelta(
                                                             days=(6 - datetime.now().weekday()))]).order_by('-date')
        for lesson in queryset:
            list_lessons.append(
                {"teacher_info": f"{lesson.teacher.last_name}.{lesson.teacher.middle_name}.{lesson.teacher.first_name}",
                 "lesson_number": lesson.number,
                 "cab": lesson.cabinet.cabinet_name,
                 "group": lesson.group.group_name,
                 "name_lesson": lesson.lesson.lesson_name,
                 "date": lesson.date}
            )
        return Response(list_lessons)


class GetAllInfoApi(APIView):
    @staticmethod
    def get(request):
        cab_list = []
        teacher_list = []
        group_list = []
        queryset_cab = Cabinet.objects.all()
        queryset_teacher = Teacher.objects.all()
        queryset_group = Group.objects.all()
        for cab in queryset_cab:
            cab_list.append(cab.cabinet_name)
        for teacher in queryset_teacher:
            teacher_list.append(f"{teacher.last_name}.{teacher.middle_name}.{teacher.first_name}")
        for group in queryset_group:
            group_list.append(group.group_name)

        response_value = {"cab": cab_list,
                          "teacher": teacher_list,
                          "group": group_list}
        return Response(response_value)
