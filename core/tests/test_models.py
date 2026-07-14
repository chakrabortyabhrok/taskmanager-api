import pytest
from core.models import Task


@pytest.mark.django_db
def test_task_creation():

    #Arrange : prepare the test data
    task = Task.objects.create(
        title = 'Test Task Creation',
        description = 'This is a test for model creation',
        status = 'todo'
    )
    # Act: (Already done in create)

    # Assert: Check if everything was saved correctly
    assert task.title == 'Test Task Creation'
    assert task.description == 'This is a test for model creation'
    assert task.id is not None

@pytest.mark.django_db
def test_task_update():

    #Arrange
    task = Task.objects.create(
        title = 'Test Task. ',
        description = 'This is a test for model update',
        status = 'todo'
    )

    #Act(Update)
    task.title = 'Test Task Updated'
    task.description = 'Updated Description'
    task.save()

    assert task.title == 'Test Task Updated'
    assert task.description == 'Updated Description'
    assert task.status == 'todo'
    