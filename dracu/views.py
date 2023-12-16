from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

news_dict = {0: {'title': "La Marató 2023",
                 'link': "https://www.ccma.cat/tv3/marato/",
                 'img': "img1.png"},
             1: {'title': "Las farmacias catalanas distribuirán productos menstruales gratuitos a partir de 2024",
                 'link': "https://elpais.com/espana/catalunya/2023-09-21/las-farmacias-catalanas-distribuiran-productos-menstruales-gratuitos-a-partir-de-2024.html#:~:text=Las%20mujeres%20catalanas%20tendr%C3%A1n%20derecho,del%20primer%20trimestre%20de%202024.",
                 'img': "img2.png"},
             2: {'title': "Cómo ayudar a tu hija a superar el miedo al uso del tampón y la copa menstrual",
                 'link': "https://elpais.com/mamas-papas/expertos/2023-08-28/como-ayudar-a-tu-hija-a-superar-el-miedo-al-uso-del-tampon-y-la-copa-menstrual.html",
                 'img': "img3.png"}}


class HealthCheckApiView(APIView):
    def get(self, request):
        # try
        # query dummy
        return Response({'status': "OK"}, status=status.HTTP_200_OK)
        # except


class NewsApiView(APIView):
    def get(self, request):
        return Response({'news': news_dict}, status=status.HTTP_200_OK)


class QuizApiView(APIView):

    def get(self, request):
        return Response({'message': "Quiz"}, status=status.HTTP_200_OK)


def generate_bard_response(message):
    new_message = message + "!!!"
    return new_message


class ChatApiView(APIView):

    def get(self, request):
        return Response({'message': "Chat"}, status=status.HTTP_200_OK)

    def post(self, request):
        received_message = request.data.get('message')

        if received_message:
            response_message = generate_bard_response(received_message)

            return Response({'message': response_message}, status=201)
        else:
            return Response({'error': "Message not provided"}, status=400)


class CameraApiView(APIView):

    def get(self, request):
        return Response({'message': "Camera"}, status=status.HTTP_200_OK)
