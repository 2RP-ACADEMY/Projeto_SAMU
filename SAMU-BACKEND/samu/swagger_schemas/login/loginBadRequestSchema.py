from drf_yasg import openapi

login_bad_request = openapi.Response(
    description='Bad Request',
    schema=openapi.Schema(
        type=openapi.TYPE_STRING
    )
)