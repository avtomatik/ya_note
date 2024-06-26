from http import HTTPStatus

from notes.forms import WARNING
from notes.models import Note
from pytils.translit import slugify

from .common import TestCaseBase


class TestLogic(TestCaseBase):

    def test_user_can_create_note(self):
        """
        Залогиненный пользователь может создать заметку, а анонимный — не
        может.

        """
        self.client.force_login(self.author)
        Note.objects.all().delete()
        notes_count_init = Note.objects.count()
        response = self.client.post(self.NOTES_ADD_URL, data=self.FORM_DATA)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_init + 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.FORM_DATA['title'])
        self.assertEqual(new_note.text, self.FORM_DATA['text'])
        self.assertEqual(new_note.slug, self.FORM_DATA['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        """
        Залогиненный пользователь может создать заметку, а анонимный — не
        может.

        """
        Note.objects.all().delete()
        notes_count_init = Note.objects.count()
        response = self.client.post(self.NOTES_ADD_URL, data=self.FORM_DATA)
        expected_url = f'{self.USERS_LOGIN_URL}?next={self.NOTES_ADD_URL}'
        self.assertRedirects(response, expected_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_init)

    def test_not_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        self.client.force_login(self.author)
        self.FORM_DATA['slug'] = self.note.slug
        notes_count_init = Note.objects.count()
        response = self.client.post(self.NOTES_ADD_URL, data=self.FORM_DATA)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_init)

    def test_empty_slug(self):
        """
        Если при создании заметки не заполнен slug, то он формируется
        автоматически, с помощью функции pytils.translit.slugify.

        """
        self.client.force_login(self.author)
        self.FORM_DATA.pop('slug')
        Note.objects.all().delete()
        notes_count_init = Note.objects.count()
        response = self.client.post(self.NOTES_ADD_URL, data=self.FORM_DATA)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_init + 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.FORM_DATA['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        """
        Пользователь может редактировать и удалять свои заметки, но не может
        редактировать или удалять чужие.

        """
        self.client.force_login(self.author)
        response = self.client.post(self.NOTES_UPDATE_URL, self.FORM_DATA)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.FORM_DATA['title'])
        self.assertEqual(self.note.text, self.FORM_DATA['text'])
        self.assertEqual(self.note.slug, self.FORM_DATA['slug'])

    def test_other_user_cant_edit_note(self):
        """
        Пользователь может редактировать и удалять свои заметки, но не может
        редактировать или удалять чужие.

        """
        self.client.force_login(self.not_author)
        response = self.client.post(self.NOTES_UPDATE_URL, self.FORM_DATA)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        """
        Пользователь может редактировать и удалять свои заметки, но не может
        редактировать или удалять чужие.

        """
        self.client.force_login(self.author)
        notes_count_init = Note.objects.count()
        response = self.client.post(self.NOTES_DELETE_URL)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count + 1, notes_count_init)

    def test_other_user_cant_delete_note(self):
        """
        Пользователь может редактировать и удалять свои заметки, но не может
        редактировать или удалять чужие.

        """
        self.client.force_login(self.not_author)
        notes_count_init = Note.objects.count()
        response = self.client.post(self.NOTES_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_init)
