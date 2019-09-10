from django.http import JsonResponse


def ok_message(message):
    return JsonResponse(
        {
            "status": 200,
            "message": message
        },
        status=200
    )


def auth_error():
    return JsonResponse(
        {
            "status": 403,
            "message": "Forbidden or No Permission to Access"
        },
        status=403
    )


def bad_request_error():
    return JsonResponse(
        {
            "status": 400,
            "message": "Bad Request"
        },
        status=400
    )
