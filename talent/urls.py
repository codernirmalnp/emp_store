from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('parental_consent/<int:talent_id>/', views.parental_consent, name='parental_consent'),
    path('profile/', views.profile, name='profile'),
    path('blog/', views.blog, name='blog'),
    path('', views.homepage, name='homepage'),
    path('blog/', views.blog, name='blog'),
    path('subscribe/', views.subscribe, name='subscribe'),
]