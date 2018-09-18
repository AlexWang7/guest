from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.test import TestCase
from sign.models import Event, Guest
from django.urls import reverse


# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1, name="一加6发布会", status=True, limit=2000, address='深圳',
                             start_time='2018-9-30 08:00:00')
        Guest.objects.create(id=1, event_id=1, real_name='alen', phone='13470467321', email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='一加6发布会')
        self.assertEqual(result.address, "深圳")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13470467321')
        self.assertEqual(result.real_name, 'alen')
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    """测试index登录首页"""

    def test_index_page_renders_index_template(self):
        """测试index视图"""
        # response=self.client.get(reverse('guest:index'))
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign/index.html')


class LoginActionTest(TestCase):
    """测试登录函数"""

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        self.c = Client()

    def test_login_action_username_password_null(self):
        """用户名密码为空"""
        test_data = {'username': '',
                     'password': ''}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'账户或密码错误', response.content.decode("utf-8"))

    def test_login_action_username_password_error(self):
        """用户密码错误"""
        test_data = {'username': 'abc',
                     'password': '123'}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'账户或密码错误', response.content.decode("utf-8"))
        # print(response.content.decode("utf-8"))

    def test_login_action_success(self):
        """登录成功"""
        test_data = {'username': 'admin',
                     'password': 'admin123456'}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    """发布会管理"""

    def setUp(self):
        Event.objects.create(id=2, name='小米8发布会', limit=2000, status=True, address="北京",
                             start_time=datetime(2018, 9, 30, 14, 0, 0))
        self.c = Client()

    def test_event_manage_success(self):
        """测试发布会小米8"""

        response = self.c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'小米8发布会', response.content.decode('utf-8'))
        self.assertIn(u'北京', response.content.decode('utf-8'))

    def test_event_manage_search_success(self):
        """测试发布会搜索"""
        response = self.c.post('/search_name/', {'name': '小米8发布会'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'北京', response.content.decode('utf-8'))


class GuestManageTest(TestCase):
    """嘉宾管理"""

    def setUp(self):
        Event.objects.create(id=1, name="小米8发布会", limit=2000, status=True,
                             address="北京", start_time=datetime(2018, 9, 30, 14, 0, 0))
        Guest.objects.create(real_name='alen', email='alen@mail.com', sign=0, phone='15998521011', event_id=1)
        self.c = Client()

    def test_event_manage_success(self):
        """测试嘉宾信息:alen"""
        response = self.c.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'alen', response.content.decode('utf-8'))
        self.assertIn(u'15998521011', response.content.decode('utf-8'))


class SignIndexActionTest(TestCase):
    """发布会签到"""

    def setUp(self):
        Event.objects.create(id=1, name="小米8发布会", status=True, limit=2000,
                             address="北京", start_time=datetime(2018, 9, 30, 10, 0, 0))
        Event.objects.create(id=2, name="一加6发布会", status=True, limit=2000,
                             address="深圳", start_time='2018-10-30 14:0:0')
        Guest.objects.create(real_name='alen', phone=15998521011,
                             email='alen@mail.com', sign=0, event_id=1)
        Guest.objects.create(real_name='una', phone=13470467350,
                             email='una@mail.com', sign=1, event_id=2)
        self.c = Client()

    def test_sign_index_action_phone_null(self):
        """手机号码为空"""
        response = self.c.post('/sign_index_action/1/', {'phone': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'号码错误', response.content.decode('utf-8'))

    def test_sign_index_action_phone_or_event_id_error(self):
        """手机号或发布会id错误"""
        response = self.c.post('/sign_index_action/2/', {'phone': '15998521011'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'号码错误或者会议号错误', response.content.decode('utf-8'))

    def test_sgin_index_user_sign_has(self):
        """用户已签到"""
        response = self.c.post('/sign_index_action/2/', {'phone': '13470467350'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'已经签过到', response.content.decode('utf-8'))

    def test_sign_index_action_sign_success(self):
        """签到成功"""
        response = self.c.post('/sign_index_action/1/', {'phone': '15998521011'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(u'签到成功', response.content.decode('utf-8'))
