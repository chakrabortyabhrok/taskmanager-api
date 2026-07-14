import pytest
from core.models import Task

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