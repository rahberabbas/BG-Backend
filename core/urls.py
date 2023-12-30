from django.urls import path
from .views import *

urlpatterns = [
    path('bg/', BackgroundApiView.as_view()),
    path('blog/', BlogListApiView.as_view()),
    path('contact/', ContactApiView.as_view()),
    path('posts/<str:slug>/', PostDetail.as_view()),
    path('cat/<str:slug>/', CaregoryListApiView.as_view()),
    path('bg/<int:pk>/', BackgroundApiView1.as_view()),
    path('bg-img/', BackgroundImageApiView.as_view()),
    path('bg-img/<int:pk>/', BackgroundImageApiView1.as_view()),
    path('bg-color/', BackgroundColorApiView.as_view()),
    path('analytics/', Analytics.as_view()),
]
