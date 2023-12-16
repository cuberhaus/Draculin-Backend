from django.urls import path
from .views import NewsApiView

urlpatterns = [
    path('news/',NewsApiView.as_view(),name='news'),
]