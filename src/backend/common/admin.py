from django.contrib import admin
from .models import SupportMessage


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
	list_display = ("id", "nickname", "is_replied", "created_at", "replied_at")
	list_filter = ("is_replied", "created_at")
	search_fields = ("nickname", "contact", "content", "reply_content")
	readonly_fields = ("is_replied", "created_at", "updated_at", "replied_at")
	fields = (
		"user",
		"nickname",
		"contact",
		"content",
		"is_replied",
		"reply_content",
		"replied_at",
		"created_at",
		"updated_at",
	)
