import pytest
from core.serializers import TaskSerializer
from models import Category

@pytest.mark.django_db
def test_category_creation():
    cat = Category.objects.create(
        name = 'Testing'
    )

    assert cat.name == 'Testing'
    assert cat.slug is not None