from django.urls import path
from .views import NewsApiView, QuizApiView, HealthCheckApiView, ChatApiView, CameraApiView

urlpatterns = [
    path('healthcheck', HealthCheckApiView.as_view(), name='healthcheck'),
    path('news/', NewsApiView.as_view(), name='news'),
    path('quiz', QuizApiView.as_view(), name='quiz'),
    path('news/', ChatApiView.as_view(), name='news'),
    path('quiz', CameraApiView.as_view(), name='quiz')
]
