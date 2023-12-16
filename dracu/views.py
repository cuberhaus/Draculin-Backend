from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

news_dict = {0: {"title": "La Marato 2023",
                 "link": "https://www.ccma.cat/tv3/marato/",
                 "img": "https://pessebre.org/wp-content/uploads/2022/12/logo-lamarato_normal.jpg"},
             1: {"title": "Las farmacias catalanas distribuiran productos menstruales gratuitos a partir de 2024",
                 "link": "https://elpais.com/espana/catalunya/2023-09-21/las-farmacias-catalanas-distribuiran-productos-menstruales-gratuitos-a-partir-de-2024.html#:~:text=Las%20mujeres%20catalanas%20tendr%C3%A1n%20derecho,del%20primer%20trimestre%20de%202024.",
                 "img": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQ1ARS6bM_n8mOlH2UjPFqSaNIxyqLSEnueI2B3-otT3VU_TRR7"},
             2: {"title": "Como ayudar a tu hija a superar el miedo al uso del tampon y la copa menstrual",
                 "link": "https://elpais.com/mamas-papas/expertos/2023-08-28/como-ayudar-a-tu-hija-a-superar-el-miedo-al-uso-del-tampon-y-la-copa-menstrual.html",
                 "img": "https://imagenes.elpais.com/resizer/uuGrWL3N7hGNPSKoNGjn49DHY5Q=/1200x0/filters:focal(2340x1430:2350x1440)/cloudfront-eu-central-1.images.arcpublishing.com/prisa/FG7RYWHKMBFGDOU2E4SX5CWAME.jpg"}}


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
        return Response({"Chat": "chat"}, status=status.HTTP_200_OK)


class CameraApiView(APIView):

    def get(self, request):
        return Response({"Camera": "camera"}, status=status.HTTP_200_OK)
