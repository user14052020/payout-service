from rest_framework.response import Response
from rest_framework.views import exception_handler

from payouts.services.exceptions import ServiceError


def service_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response

    if isinstance(exc, ServiceError):
        return Response({"detail": str(exc)}, status=400)

    return response
