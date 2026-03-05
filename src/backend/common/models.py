from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SupportMessage(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="support_messages")
	nickname = models.CharField(max_length=50)
	contact = models.CharField(max_length=100, blank=True, default="")
	content = models.TextField()

	is_replied = models.BooleanField(default=False)
	reply_content = models.TextField(blank=True, default="")
	replied_at = models.DateTimeField(null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]
		verbose_name = "客服留言"
		verbose_name_plural = "客服留言"

	def save(self, *args, **kwargs):
		has_reply = bool(str(self.reply_content).strip())
		if has_reply:
			self.is_replied = True
			if self.replied_at is None:
				self.replied_at = timezone.now()
		else:
			self.is_replied = False
			self.replied_at = None
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.nickname} - {self.content[:20]}"
