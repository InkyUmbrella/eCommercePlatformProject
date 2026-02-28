class AppException(Exception):
    """业务异常基类。"""

    def __init__(self, message="业务异常", code=10000, status=400, data=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status
        self.data = data if data is not None else {}
