import django
django.setup()
from django.test import TestCase
import pytest
from django.core.exceptions import ValidationError
from .models import Username, Task, UsernameForm

@pytest.mark.django_db
def test_username_model_create():
    # Test creating a Username object
    username = Username.objects.create(username='test_user')
    assert username.username == 'test_user'

@pytest.mark.django_db
def test_task_model_create():
    # Test creating a Task object
    username = Username.objects.create(username='test_user')
    task = Task.objects.create(username=username, title='Test Task', description='This is a test task')
    assert task.title == 'Test Task'
    assert task.description == 'This is a test task'

@pytest.mark.django_db
def test_username_form_clean_username_unique():
    # Test clean_username method of UsernameForm for unique username
    form_data = {'username': 'unique_username'}
    form = UsernameForm(data=form_data)
    assert form.is_valid()
    assert form.clean_username() == 'unique_username'

#@pytest.mark.django_db
#def test_username_form_clean_username_not_unique():
#    Username.objects.create(username='test_username')
#    form_data = {'username': 'test_username'}
#    form = UsernameForm(data=form_data)
#    with pytest.raises(ValidationError) as e:
#        form.is_valid()
#        form.clean_username()
#    assert str(e.value) == 'This username is already taken! Try a different one :)'
