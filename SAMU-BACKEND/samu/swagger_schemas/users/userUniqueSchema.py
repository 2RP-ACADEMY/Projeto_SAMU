from drf_yasg import openapi

userUniqueSchema = openapi.Schema(
    title="Succesfull schema",
    type=openapi.TYPE_OBJECT,
    properties={
        "detail": openapi.Schema(type=openapi.TYPE_STRING),
        "object": openapi.Schema(type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "is_staff": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "is_superuser": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN)
            }
        )
    }
)