from django.test import TestCase

from django.test.client import Client
from .factories import *
from .api.views.general_views import *

class UserTestCase(TestCase):

    def setUp(self):
        self.user = UserCommonFactory()
        self.user_admin = UserAdminFactory()
        self.task = TaskFactory()
        self.client = Client()

        
    def test_common_user_creation(self):
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.id)

    def test_admin_user_creation(self):
        self.assertTrue(self.user_admin.is_active)
        self.assertTrue(self.user_admin.is_staff)
        self.assertTrue(self.user_admin.is_superuser)
    

    def test_task_creation(self):
        password = self.user.password
        self.user.set_password(password)
        self.user.save()
        self.task.user = self.user
        self.task.save()
        self.assertIsNotNone(self.task.id)
        self.assertIsNotNone(self.task.user)
        self.assertEqual(self.task.user.username, self.user.username)
        
        
    def test_login(self):
        password = self.user.password
        self.user.set_password(password)
        self.user.save()
        response = self.client.login(username = self.user.username, password = password)
        self.assertTrue(response)

    def test_login_fail(self):
        password = self.user.password
        self.user.set_password(password)
        self.user.save()
        response = self.client.login(username = self.user.username, password = 'claveincorrecta')
        self.assertFalse(response)

    def test_logout(self):
        password = self.user.password
        self.user.set_password(password)
        self.user.save()
        response = self.client.login(username = self.user.username, password = password)
        self.assertTrue(response)
        response = self.client.logout()

    def test_security_gets(self):
        response = self.client.get('/users/')
        self.assertEquals(response.status_code, 400)

        response = self.client.get('/users/1/')
        self.assertEquals(response.status_code, 400)

        response = self.client.get('/tasks/')
        self.assertEquals(response.status_code, 400)

        response = self.client.get('/tasks/1/')
        self.assertEquals(response.status_code, 400)

        response = self.client.get('/tasks/user/')
        self.assertEquals(response.status_code, 400)

    def test_security_posts(self):
        response = self.client.post('/users/')
        self.assertEquals(response.status_code, 400)

        response = self.client.post('/tasks/')
        self.assertEquals(response.status_code, 400)

    def test_security_puts(self):
        response = self.client.put('/users/1/')
        self.assertEquals(response.status_code, 400)

        response = self.client.put('/tasks/1/')
        self.assertEquals(response.status_code, 400)

    def test_security_deleteds(self):
        response = self.client.delete('/users/1/')
        self.assertEquals(response.status_code, 400)

        response = self.client.delete('/tasks/1/')
        self.assertEquals(response.status_code, 400)