from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

# The pagination class is now set in the test settings, so views will use it by default.

class MockView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"foo": "bar"})

class PaginatedView(GenericAPIView):
    queryset = list(range(100))

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)
        return Response(queryset)

class ErrorView(APIView):
    def get(self, request, *args, **kwargs):
        error_type = request.query_params.get('type', 'validation')

        if error_type == 'validation':
            raise ValidationError({
                'field1': ['This field is required'],
                'field2': ['This field must be unique']
            })
        elif error_type == 'not_found':
            raise NotFound('Resource not found')
        elif error_type == 'permission':
            raise PermissionDenied('You do not have permission to perform this action')
        else:
            # Generic exception
            raise Exception('Unexpected error')

class PreformattedResponseView(APIView):
    def get(self, request, *args, **kwargs):
        # Return a response that's already in the standard format
        return Response({
            "success": True,
            "message": "Pre-formatted response",
            "data": {"test": "value"}
        })

urlpatterns = [
    path('api/mock/', MockView.as_view(), name='mock-view'),
    path('api/paginated/', PaginatedView.as_view(), name='paginated-view'),
    path('api/error/', ErrorView.as_view(), name='error-view'),
    path('api/preformatted/', PreformattedResponseView.as_view(), name='preformatted-view'),
]
