from rest_framework import serializers, exceptions

from django_testing import settings
from models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")
    def vaidate_students(self, value):
        if len(value) > settings.MAX_STUDENTS_PER_COURSE:
            raise exceptions.ValidationError("Превышено максимальное количество студентов")
        return value