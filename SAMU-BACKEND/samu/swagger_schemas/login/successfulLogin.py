from drf_yasg import openapi

successful_login = openapi.Response(
    description='Successful login',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING, description='Access Token'),
        }
    )
)