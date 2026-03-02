from rest_framework.response import Response

def ok(data=None, message="success", code=0, status_code=200):
    return Response({
        "code": code,
        "message": message,
        "data": data
    }, status=status_code)

def fail(message="fail", code=1, data=None, http_status=400):
    return Response({
        "code": code,
        "message": message,
        "data": data
    }, status=http_status)