from drf_yasg import openapi

groupListSchema = openapi.Schema(
    title="Succesfull schema",
    type=openapi.TYPE_OBJECT,
    properties={
        "detail": openapi.Schema(type=openapi.TYPE_STRING),
        "object": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "name": openapi.Schema(type=openapi.TYPE_STRING)
            })
        )
    }
)