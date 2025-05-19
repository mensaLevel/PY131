import pytest
import factory
from django.urls import reverse
from django.utils import timezone
from django.forms.models import model_to_dict
from datetime import date, time

#pip install pytest pytest-django pytest-cov factory-boy
#pytest.ini
# [pytest]
# DJANGO_SETTINGS_MODULE = myproject.settings
# python_files = test_*.py *_test.py tests.py
# filterwarnings = ignore::django.utils.deprecation.RemovedInDjango50Warning



from .models import Category
from .forms import NoteForm


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker('text', max_nb_chars=200)


@pytest.fixture
def category():
    return CategoryFactory() 


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(
        title ='PyTestTitle',
    )

    assert category.id is not None
    assert category.title == 'PyTestTitle'

    form_data = {
        'title': "PytestTitle",
        'text': 'Beetroot',
        'reminder': "2025-05-20",
        'category': category.id,  
        }

    form = NoteForm(data=form_data)
    assert form.is_valid()
