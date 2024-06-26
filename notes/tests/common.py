from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestCaseBase(TestCase):

    NOTES_ADD_URL = reverse('notes:add')
    NOTES_HOME_URL = reverse('notes:home')
    NOTES_LIST_URL = reverse('notes:list')
    NOTES_SUCCESS_URL = reverse('notes:success')
    USERS_LOGIN_URL = reverse('users:login')
    USERS_LOGOUT_URL = reverse('users:logout')
    USERS_SIGNUP_URL = reverse('users:signup')

    FORM_DATA = {
        'title': 'Заголовок',
        'text': 'Текст',
        'slug': 'Slug',
    }

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Автор')
        cls.not_author = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='Slug',
            author=cls.author
        )

        cls.NOTES_DETAIL_URL = reverse('notes:detail', args=(cls.note.slug,))
        cls.NOTES_UPDATE_URL = reverse('notes:edit', args=(cls.note.slug,))
        cls.NOTES_DELETE_URL = reverse('notes:delete', args=(cls.note.slug,))
