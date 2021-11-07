from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('register/', views.register_view, name="register_view"),
    path('funding/', views.funding, name="funding"),
    path('generate_signature/', views.SignatureGenerator.as_view(), name="generate_signature"),
    path('hook/', views.webhook_reciever, name="webhook_reciever"),
    path('dashboard/', views.home_page, name="home_page"),
]
