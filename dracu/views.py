from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

news_dict = {0: "BitsxlaMarato 2023",
             1: "Las farmacias catalanas distribuirán productos menstruales gratuitos a partir de 2024",
             2: "Draculito"}


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
