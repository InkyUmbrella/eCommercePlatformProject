from django.http import JsonResponse


def api_success(data=None, message="success", code=0, status=200):
    """统一成功返回体。"""
    return JsonResponse(
        {
            "code": code,
            "message": message,
            "data": data if data is not None else {},
        },
        status=status,
    )


def api_error(message="error", code=10000, data=None, status=400):
    """统一失败返回体。"""
    return JsonResponse(
        {
            "code": code,
            "message": message,
            "data": data if data is not None else {},
        },
        status=status,
    )
