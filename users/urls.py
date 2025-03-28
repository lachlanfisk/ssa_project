from django.urls import path
from . import views

urlpatterns = [
    path("", views.user, name="user"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
<<<<<<< HEAD
    path('top-up/', views.top_up, name='top_up'),
    path('top-up/<int:user_id>/', views.top_up, name='top_up'),
    path('delete_account/', views.delete_account, name='delete_account'),
=======
>>>>>>> 7faa12264b3d22f5d5da482278a01edd8a6e2c1f
]