from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', LogoutView.as_view(), name='logout'),  # ✅ nome definido corretamente
]
