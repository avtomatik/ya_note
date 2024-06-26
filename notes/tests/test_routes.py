from http import HTTPStatus

from .common import TestCaseBase


class TestRoutes(TestCaseBase):

    def test_pages_availability_for_anonymous_user(self):
        """
        Главная страница доступна анонимному пользователю.

        Страницы регистрации пользователей, входа в учётную запись и выхода из
        неё доступны всем пользователям.

        """
        for url in (
            self.NOTES_HOME_URL,
            self.USERS_LOGIN_URL,
            self.USERS_LOGOUT_URL,
            self.USERS_SIGNUP_URL,
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        """
        Аутентифицированному пользователю доступна страница со списком заметок
        notes/, страница успешного добавления заметки done/, страница
        добавления новой заметки add/.

        """
        self.client.force_login(self.not_author)
        for url in (
            self.NOTES_ADD_URL,
            self.NOTES_LIST_URL,
            self.NOTES_SUCCESS_URL,
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        """
        Страницы отдельной заметки, удаления и редактирования заметки доступны
        только автору заметки. Если на эти страницы попытается зайти другой
        пользователь — вернётся ошибка 404.

        """
        users_statuses = (
            (self.not_author, HTTPStatus.NOT_FOUND),
            (self.author, HTTPStatus.OK),
        )
        for user, status_code in users_statuses:
            self.client.force_login(user)
            for url in (
                self.NOTES_DETAIL_URL,
                self.NOTES_UPDATE_URL,
                self.NOTES_DELETE_URL,
            ):
                with self.subTest(url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status_code)

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
