import pytest
import factory
from django.utils import timezone
from .models import Category, Note
from .forms import NoteForm


#pip install pytest pytest-django pytest-cov factory-boy
#pytest.ini
# [pytest]
# DJANGO_SETTINGS_MODULE = myproject.settings
# python_files = test_*.py *_test.py tests.py
# filterwarnings = ignore::django.utils.deprecation.RemovedInDjango50Warning

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker('sentence', nb_words=4)

class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    title = factory.Faker('sentence', nb_words=4)
    text = factory.Faker('sentence', nb_words=4)
    reminder = factory.LazyFunction(timezone.now)
    category = factory.SubFactory(CategoryFactory)



@pytest.fixture
def category():
    return CategoryFactory() 

@pytest.fixture
def note():
    return NoteFactory() 

@pytest.mark.django_db
def test_note_form_valid(note, category):
    form_data = {
        'title': note.title,
        'text': note.text,
        'reminder': note.reminder,
        'category': category,
    }
    form = NoteForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_create_note(category):
    start_count = Note.objects.count()
    note = Note.objects.create(title="Test Note", text="Some text", reminder="2025-05-20", category=category)
    assert Note.objects.count() - start_count == 1
    note.delete()

@pytest.mark.django_db
def test_update_note(category, note):
    note.title = 'Updated Title'
    note.text = 'Updated Text'
    note.reminder = '2025-05-20'
    category = 'Новина'
    note.save()
    assert note.title == 'Updated Title'
    assert note.text == 'Updated Text'
    assert note.reminder == '2025-05-20'
    assert category == 'Новина'

@pytest.mark.django_db
def test_delete_note(category):
    note = Note.objects.create(title="To Be Deleted", text="Some text", reminder="2025-05-20", category=category)
    note_id = note.id
    note.delete()
    assert not Note.objects.filter(id=note_id).exists()

@pytest.mark.django_db
def test_view_note(note):
    fetched_note = Note.objects.get(id=note.id)
    assert fetched_note.text == note.text