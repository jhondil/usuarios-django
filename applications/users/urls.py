
from django.urls import path
from . import views

app_name = "user_app"

urlpatterns = [
    path(
        'register/', 
        views.UserRegisterView.as_view(),
        name='user-register'
        ),
    path(
        'login/', 
        views.LoginUser.as_view(),
        name='login'
        ),
    path(
        'logout/', 
        views.logoutView.as_view(),
        name='logout'
        ),
    path(
        'update/', 
        views.UpdatePasswordView.as_view(),
        name='actualizar'
        ),
    path(
        'verifications/<pk>/', 
        views.CodVerificacionView.as_view(),
        name='verificacion'
        ),
]
