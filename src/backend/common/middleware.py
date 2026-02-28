from django.http import JsonResponse

from .exceptions import AppException


class GlobalExceptionMiddleware:
    """全局异常处理：把异常转成统一 JSON 返回。"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except AppException as exc:
            return JsonResponse(
                {
                    "code": exc.code,
                    "message": exc.message,
                    "data": exc.data,
                },
                status=exc.status,
            )
        except Exception:
            return JsonResponse(
                {
                    "code": 50000,
                    "message": "服务器内部错误",
                    "data": {},
                },
                status=500,
            )
