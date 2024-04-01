from drf_yasg import openapi

errorSchema = openapi.Schema(
    title="Error schema",
    type=openapi.TYPE_OBJECT,
    properties={
        "detail": openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            properties={
                "error_name": openapi.Schema(type=openapi.TYPE_STRING),
                "error_cause": openapi.Schema(type=openapi.TYPE_ARRAY, 
                                        items=openapi.Schema(type=openapi.TYPE_STRING))
            }
        )
    }
)
