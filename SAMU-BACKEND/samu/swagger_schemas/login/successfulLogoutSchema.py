from drf_yasg import openapi

successful_logout = openapi.Response(
    description='Successful logout',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )
)