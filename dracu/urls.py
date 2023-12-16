from django.urls import path
from .views import NewsApiView, QuizApiView, HealthCheckApiView, ChatApiView, CameraApiView

urlpatterns = [
    path('healthcheck/', HealthCheckApiView.as_view(), name='healthcheck'),
    path('stats/', StatsApiView.as_view(), name='stats'),
    path('news/', NewsApiView.as_view(), name='news'),
    path('quiz', QuizApiView.as_view(), name='quiz'),
    path('chat/', ChatApiView.as_view(), name='chat'),
    path('camera/', CameraApiView.as_view(), name='camera')
]
