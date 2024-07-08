import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student

def test_example():
    assert False, "Just test example"





@pytest.fixture
def client_api():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory()
@pytest.mark.django_db
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory()

@pytest.mark.django_db
def get_first_course(client_api, course_factory):
    course = course_factory(_quantiti=1)
    course_id = course[0].id

    response = client_api.get(f"/api/v1/courses/{course_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == course[0].name


@pytest.mark.django_db
def get_list_courses(client_api, course_factory):
    course = course_factory(_quantiti=3)
    response = client_api.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)

    for i,m in enumerate(data):
        assert m["name"] == course[i].name


@pytest.mark.django_db
def filter_by_id(client_api, course_factory):
    course = course_factory(_quantiti=3)
    course_id = course[0].id
    response = client_api.get(f"/api/v1/courses/?id={course_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == course[0].name


@pytest.mark.django_db
def get_filter_by_name(client_api, course_factory):
    course = course_factory(_quantiti=3)
    course_name = course[0].name
    response = client_api.get(f"/api/v1/courses/?name={course_name}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    for i, m in enumerate(data):
        assert m["name"] == course[i].name

@pytest.mark.django_db
def post_course(client_api):
    student_1 = Student.objects.create(name = "Vasya", birth_date = "2000-01-01")
    student_2 =Student.objects.create(name = "Petya", birth_date = "2004-01-01")
    response = client_api.post(
        "/api/v1/courses/",
        data = {
            "name": "Python",
            "students": [student_1.id, student_2.id]
        }
    )
    assert response.status_code == 201

@pytest.mark.django_db
def post_course_1(client_api, student_factory):
    students = student_factory(_quantiti=2)
    response = client_api.post(
        "/api/v1/courses/",
        data = {
            "name": "Python",
            "students": [i.id for i in students]
        }
    )
    assert response.status_code == 201
@pytest.mark.django_db
def test_pach_course(client_api, course_factory):
    student = Student.objects.create(name = "Misha", birth_date = "2000-01-07")
    course = course_factory(_quantiti=1)
    course_id = course[0].id
    response = client_api.patch(
        f"/api/v1/courses/{course_id}/",
        data = {
            "name": "Python",
            "students": [student.id]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["students"] == [student.id]
@pytest.mark.django_db
def test_delete_course(client_api, course_factory):
    course = course_factory(_quantiti=1)
    course_id = course[0].id
    response = client_api.delete(f"/api/v1/courses/{course_id}/")
    assert response.status_code == 204


@pytest.mark.parametrize('max_count, students_count, response_status', [(20,25,100), (20,30,200), (20,20,200)])
@pytest.mark.django_db
def test_max_student(settings, max_count, students_count, response_status, client_api, student_factory):
    settings.MAX_STUDENTS_PER_COURSE = max_count
    students = student_factory(_quantiti=students_count)
    response = client_api.get("/api/v1/courses/", data = {"students": [i.id for i in students]})
    assert response.status_code == response_status