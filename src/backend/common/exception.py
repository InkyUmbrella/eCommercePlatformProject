import logging
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    统一异常返回结构：
    {
      "code": 业务码,
      "message": "错误信息",
      "data": ...
    }
    """
    response = exception_handler(exc, context)

    # 1) DRF 已识别的异常
    if response is not None:
        # 提取 message
        detail = response.data
        if isinstance(detail, dict):
            if "detail" in detail:
                message = str(detail["detail"])
            else:
                message = "; ".join([f"{k}:{v}" for k, v in detail.items()])
        elif isinstance(detail, list):
            message = "; ".join([str(x) for x in detail])
        else:
            message = str(detail)

        response.data = {
            "code": response.status_code,
            "message": message,
            "data": None,
        }
        return response

    # 2) 未识别异常
    logger.exception("Unhandled exception", exc_info=exc)
    return Response(
        {
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "服务器内部错误",
            "data": None,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )