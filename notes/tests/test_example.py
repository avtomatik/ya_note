from http import HTTPStatus

import pytest

from notes.models import Note


def test_with_client(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_closed_page(admin_client):
    response = admin_client.get('/only-for-users/')
    assert response.status_code == HTTPStatus.OK

# =============================================================================
# Option: admin_user
# =============================================================================


def test_with_authenticated_client(django_user_model):
    user = django_user_model.objects.create(username='yanote_user')


def test_with_authenticated_client(client, django_user_model):
    user = django_user_model.objects.create(username='yanote_user')
    client.force_login(user)
    response = client.get('/private/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.skip(reason='Demonstration Only')
def test_note_exists(note):
    notes_count = Note.objects.count()
    assert notes_count == 1
    assert note.title == 'Заголовок'


@pytest.mark.skip(reason='Demonstration Only')
@pytest.mark.django_db
def test_empty_db():
    notes_count = Note.objects.count()
    assert notes_count == 0
