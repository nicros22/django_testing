from django.test import TestCase
from django.urls import reverse

from notes.models import Note, User


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create(username='Читатель простой')
        cls.author = User.objects.create(username='Лев Толстой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.author,
        )

    def test_note_list_for_different_users(self):
        users_notes = (
            (self.author, True),
            (self.reader, False),
        )
        url = reverse('notes:list')
        for user, note_list in users_notes:
            self.client.force_login(user)
            with self.subTest(user=user.username, note_list=note_list):
                response = self.client.get(url)
                note_in_object = self.note in response.context['object_list']
                self.assertEqual(note_in_object, note_list)

    def test_existing_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for page, args in urls:
            with self.subTest(page=page):
                url = reverse(page, args=args)
                self.client.force_login(self.author)
                response = self.client.get(url)
                self.assertIn('form', response.context)
