from http import HTTPStatus

from .common import TestCaseBase


class TestRoutes(TestCaseBase):

    def test_pages_availability(self):
        """
        Главная страница доступна анонимному пользователю.

        Страницы регистрации пользователей, входа в учётную запись и выхода из
        неё доступны всем пользователям.

        Аутентифицированному пользователю доступна страница со списком заметок
        notes/, страница успешного добавления заметки done/, страница
        добавления новой заметки add/.

        Страницы отдельной заметки, удаления и редактирования заметки доступны
        только автору заметки. Если на эти страницы попытается зайти другой
        пользователь — вернётся ошибка 404.

        """
        for client, url, expected_status in (
            (self.client, self.NOTES_HOME_URL, HTTPStatus.OK),
            (self.client, self.USERS_LOGIN_URL, HTTPStatus.OK),
            (self.client, self.USERS_LOGOUT_URL, HTTPStatus.OK),
            (self.client, self.USERS_SIGNUP_URL, HTTPStatus.OK),
            (self.not_author_client, self.NOTES_ADD_URL, HTTPStatus.OK),
            (self.not_author_client, self.NOTES_LIST_URL, HTTPStatus.OK),
            (self.not_author_client, self.NOTES_SUCCESS_URL, HTTPStatus.OK),
            (
                self.not_author_client,
                self.NOTES_DETAIL_URL,
                HTTPStatus.NOT_FOUND
            ),
            (
                self.not_author_client,
                self.NOTES_UPDATE_URL,
                HTTPStatus.NOT_FOUND
            ),
            (
                self.not_author_client,
                self.NOTES_DELETE_URL,
                HTTPStatus.NOT_FOUND
            ),
            (self.author_client, self.NOTES_DETAIL_URL, HTTPStatus.OK),
            (self.author_client, self.NOTES_UPDATE_URL, HTTPStatus.OK),
            (self.author_client, self.NOTES_DELETE_URL, HTTPStatus.OK),
        ):
            with self.subTest(
                client=client, url=url, expected_status=expected_status
            ):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_client(self):
        """
        При попытке перейти на страницу списка заметок, страницу успешного
        добавления записи, страницу добавления заметки, отдельной заметки,
        редактирования или удаления заметки анонимный пользователь
        перенаправляется на страницу логина.

        """
        for url in (
            self.NOTES_ADD_URL,
            self.NOTES_DELETE_URL,
            self.NOTES_DETAIL_URL,
            self.NOTES_LIST_URL,
            self.NOTES_SUCCESS_URL,
            self.NOTES_UPDATE_URL,
        ):
            with self.subTest(url=url):
                redirect_url = f'{self.USERS_LOGIN_URL}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
