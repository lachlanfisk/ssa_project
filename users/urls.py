from django.urls import path
from . import views

urlpatterns = [
    path("", views.user, name="user"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('top-up/', views.top_up, name='top_up'),
    path('top-up/<int:user_id>/', views.top_up, name='top_up'),
    path('delete_account/', views.delete_account, name='delete_account'),
]