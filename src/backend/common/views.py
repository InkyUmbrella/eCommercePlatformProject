from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from common.response import ok, fail
from .models import SupportMessage


def _serialize_message(item):
	return {
		"id": item.id,
		"nickname": item.nickname,
		"content": item.content,
		"is_replied": item.is_replied,
		"reply_content": item.reply_content,
		"created_at": item.created_at.isoformat(),
		"replied_at": item.replied_at.isoformat() if item.replied_at else None,
	}


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def support_messages(request):
	if request.method == "GET":
		queryset = SupportMessage.objects.all().order_by("-created_at")[:50]
		return ok([_serialize_message(item) for item in queryset])

	nickname = str(request.data.get("nickname", "")).strip()
	contact = str(request.data.get("contact", "")).strip()
	content = str(request.data.get("content", "")).strip()

	if not content:
		return fail("content 必填", http_status=400)

	user = request.user if getattr(request, "user", None) and request.user.is_authenticated else None
	if not nickname:
		nickname = user.username if user else "匿名用户"

	item = SupportMessage.objects.create(
		user=user,
		nickname=nickname,
		contact=contact,
		content=content,
	)

	return ok(_serialize_message(item), "留言提交成功")
