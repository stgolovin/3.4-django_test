import pytest

from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_first_course(client, course_factory):
    courses = course_factory(_quantity=2)
    response = client.get(f'/api/v1/courses/{courses[0].id}/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses[0].name


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    for id, course in enumerate(courses):
        assert data[id]['name'] == courses[id].name


@pytest.mark.django_db
def test_filter_courses_id(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?id={courses[0].id}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[0].id


@pytest.mark.django_db
def test_filter_courses_name(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/?name={courses[0].name}')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_create_course(client):
    course = {'name': 'c++'}
    response = client.post('/api/v1/courses/', data=course)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == course['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=1)
    course_data = {"name": "css"}
    response = client.patch(f'/api/v1/courses/{course[0].id}/', data=course_data)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course_data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=2)
    count = Course.objects.count()
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    client.delete(f'/api/v1/courses/{course[0].id}/')
    assert Course.objects.count() == count - 1