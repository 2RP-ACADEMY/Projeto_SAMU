from drf_yasg import openapi 

errorSchema401 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "detail": openapi.Schema(type=openapi.TYPE_STRING)
    }
)
    
