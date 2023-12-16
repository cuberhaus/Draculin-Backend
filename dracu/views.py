from django.shortcuts import render

# Create your views here.
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import bard_api

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
        # try
        # query dummy
        return Response({'status': "OK"}, status=status.HTTP_200_OK)
        # except


class StatsApiView(APIView):
    def get(self, request):
        return Response({'stats': "stats"}, status=status.HTTP_200_OK)


class NewsApiView(APIView):
    def get(self, request):
        return Response({'news': news_dict}, status=status.HTTP_200_OK)


class QuizApiView(APIView):

    def get(self, request):
        return Response({'message': "Quiz"}, status=status.HTTP_200_OK)


def generate_bard_response(bard, message):
    bard, new_message = bard_api.ask(bard, message)
    return bard, new_message


class ChatApiView(APIView):
    def get(self, request):
        bard = cache.get('bard-model')
        # Init bard and store it into cache
        bard, prompt = bard_api.init()
        cache.set('bard-model', bard)

        # Init messages_dict and store it into cache
        messages_dict = {0: prompt}
        cache.set('messages-dict', messages_dict)

        return Response({'messages_dict': messages_dict, 'message': prompt}, status=status.HTTP_200_OK)

    def post(self, request):
        bard = cache.get('bard-model')
        messages_dict = cache.get('messages-dict')
        message = request.data.get('message')

        # Update messages_dict and store it into cache
        messages_dict[len(messages_dict)] = message
        cache.set('messages-dict', messages_dict)

        if message:
            bard, response_message = generate_bard_response(bard, message)

            # Store bard in cache
            cache.set('bard-model', bard)

            # Update messages_dict and store it into cache
            messages_dict[len(messages_dict)] = response_message
            cache.set('messages-dict', messages_dict)

            return Response({'messages_dict': messages_dict, 'message': response_message}, status=201)
        else:
            return Response({'error': "Message not provided"}, status=400)


class CameraApiView(APIView):

    def get(self, request):
        return Response({'message': "Camera"}, status=status.HTTP_200_OK)

    def post(self, request):
        photo = request.data.get('photo')

        if photo:
            # Send photo to model

            # get model punctuation
            punctuation = 0

            return Response({'photo': photo, 'punctuation': punctuation}, status=201)
        else:
            return Response({'error': "Photo not provided"}, status=400)


class MessagesApiView(APIView):

    def get(self, request):
        messages_dict = cache.get('messages-dict')
        return Response({'messages_dict': messages_dict}, status=status.HTTP_200_OK)
