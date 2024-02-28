import pytest
import django
django.setup()
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task


@pytest.fixture
def user_client(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.force_login(user)
    return client

@pytest.fixture
def create_task():
    def _create_task(user):
        return Task.objects.create(user=user, title='Test Task', completed=False)
    return _create_task

def test_task_creation(user_client, create_task):
    response = user_client.post(reverse('todo:new_task'), {'title': 'Test Task'})
    assert response.status_code == 302
    assert Task.objects.filter(title='Test Task').exists()

def test_task_update(user_client, create_task):
    task = create_task(user_client.user)
    response = user_client.post(reverse('todo:update_task', kwargs={'pk': task.pk}), {'title': 'Updated Task'})
    assert response.status_code == 302
    task.refresh_from_db()
    assert task.title == 'Updated Task'

def test_task_deletion(user_client, create_task):
    task = create_task(user_client.user)
    response = user_client.post(reverse('todo:delete_task', kwargs={'pk': task.pk}))
    assert response.status_code == 302
    assert not Task.objects.filter(pk=task.pk).exists()

def test_task_completion(user_client, create_task):
    task = create_task(user_client.user)
    response = user_client.post(reverse('todo:complete_task', kwargs={'pk': task.pk}))
    assert response.status_code == 302
    task.refresh_from_db()
    assert task.completed == True

def test_task_list(user_client, create_task):
    task = create_task(user_client.user)
    response = user_client.get(reverse('todo:task_list'))
    assert response.status_code == 200
    assert task.title.encode() in response.content
