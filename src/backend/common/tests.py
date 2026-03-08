from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import SupportMessage


class SupportMessageApiTests(APITestCase):
	def test_submit_message_success(self):
		response = self.client.post(
			"/api/support/messages/",
			{
				"nickname": "访客A",
				"contact": "test@example.com",
				"content": "请问什么时候发货？",
			},
			format="json",
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["code"], 0)
		self.assertEqual(response.data["data"]["nickname"], "访客A")
		self.assertEqual(response.data["data"]["content"], "请问什么时候发货？")
		self.assertFalse(response.data["data"]["is_replied"])

	def test_reply_requires_auth(self):
		message = SupportMessage.objects.create(nickname="匿名用户", content="待回复")

		response = self.client.patch(
			f"/api/support/messages/{message.id}/reply/",
			{"reply_content": "已收到"},
			format="json",
		)

		self.assertEqual(response.status_code, 401)

	def test_non_staff_cannot_reply(self):
		message = SupportMessage.objects.create(nickname="匿名用户", content="待回复")
		user = User.objects.create_user(username="normal_user", password="pwd123456")
		token = str(RefreshToken.for_user(user).access_token)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

		response = self.client.patch(
			f"/api/support/messages/{message.id}/reply/",
			{"reply_content": "不允许"},
			format="json",
		)

		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.data["code"], 1)

	def test_staff_reply_success_and_list_visible(self):
		message = SupportMessage.objects.create(nickname="匿名用户", content="待回复")
		staff = User.objects.create_user(username="support_admin", password="pwd123456", is_staff=True)
		token = str(RefreshToken.for_user(staff).access_token)
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

		reply_response = self.client.patch(
			f"/api/support/messages/{message.id}/reply/",
			{"reply_content": "您好，今天会发货。"},
			format="json",
		)

		self.assertEqual(reply_response.status_code, 200)
		self.assertEqual(reply_response.data["code"], 0)
		self.assertTrue(reply_response.data["data"]["is_replied"])
		self.assertEqual(reply_response.data["data"]["reply_content"], "您好，今天会发货。")
		self.assertIsNotNone(reply_response.data["data"]["replied_at"])

		self.client.credentials()
		list_response = self.client.get("/api/support/messages/")

		self.assertEqual(list_response.status_code, 200)
		self.assertEqual(list_response.data["code"], 0)
		self.assertGreaterEqual(len(list_response.data["data"]), 1)
		self.assertTrue(list_response.data["data"][0]["is_replied"])
