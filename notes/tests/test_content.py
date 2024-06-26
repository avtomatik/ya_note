from notes.forms import NoteForm

from .common import TestCaseBase


class TestContent(TestCaseBase):

    def test_note_in_list_for_different_users(self):
        """
        Отдельная заметка передаётся на страницу со списком заметок в списке
        object_list, в словаре context.

        В список заметок одного пользователя не попадают заметки другого
        пользователя.

        """
        users_values = (
            (self.author, True),
            (self.not_author, False)
        )
        for user, value in users_values:
            self.client.force_login(user)
            response = self.client.get(self.NOTES_LIST_URL)
            object_list = response.context['object_list']
            self.assertEqual(self.note in object_list, value)

    def test_pages_contain_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        self.client.force_login(self.author)
        for url in (
            self.NOTES_ADD_URL,
            self.NOTES_UPDATE_URL
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
