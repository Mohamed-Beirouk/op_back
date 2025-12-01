from django.urls import path
from .views import create_object_perdus, list_categories, list_objects_perdus, my_objects_perdus, register, return_object_perdus
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('api/', include('op_app.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('categories/', list_categories, name='categories'),
    path('objects_perdus/', list_objects_perdus, name='objects_perdus'),
    path('create_object_perdus/', create_object_perdus, name='create_object_perdus'),
    path('return_object_perdus/<int:op_id>/', return_object_perdus, name='return_object_perdus'),
    path('my_objects_perdus/', my_objects_perdus, name='my_objects_perdus'),

]