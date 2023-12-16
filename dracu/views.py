from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

news_dict = {0: "new0", 1: "new1", 2: "new2"}


class HealthCheckApiView(APIView):
    def get(self, request):
        return Response("Health Check", status=status.HTTP_200_OK)


class NewsApiView(APIView):
    def get(self, request):
        return Response({"news": news_dict}, status=status.HTTP_200_OK)


class QuizApiView(APIView):

    def get(self, request):
        return Response("Quiz", status=status.HTTP_200_OK)


class ChatApiView(APIView):

    def get(self, request):
        return Response({"Chat": news_dict}, status=status.HTTP_200_OK)


class CameraApiView(APIView):

    def get(self, request):
        return Response({"Camera": news_dict}, status=status.HTTP_200_OK)
