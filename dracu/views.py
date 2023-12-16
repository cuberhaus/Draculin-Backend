from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class NewsApiView(APIView):
    def get(self,request):
        return Response({"message":"Test"},status=status.HTTP_200_OK)