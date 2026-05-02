import base64
import io
import mimetypes
from pathlib import Path

from django.shortcuts import render
from django.core.cache import cache
from django.http import FileResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from PIL import Image

STATIC_DIR = Path(__file__).resolve().parent.parent / 'static'


def serve_static(request, path):
    file_path = STATIC_DIR / path
    if not file_path.is_file() or not file_path.resolve().is_relative_to(STATIC_DIR):
        raise Http404
    content_type, _ = mimetypes.guess_type(str(file_path))
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Access-Control-Allow-Origin'] = '*'
    return response

try:
    import bard_api
    HAS_BARD = True
except ImportError:
    HAS_BARD = False

try:
    from dracu.inference_image import get_blood_ratio
    HAS_VISION = True
except ImportError:
    HAS_VISION = False

try:
    from dracu.serializers import ImageSerializer
except ImportError:
    pass

news_dict = {0: {"title": "La Marato 2023",
                 "link": "https://www.ccma.cat/tv3/marato/",
                 "img": "/media/news/marato.jpg"},
             1: {"title": "Las farmacias catalanas distribuiran productos menstruales gratuitos a partir de 2024",
                 "link": "https://elpais.com/espana/catalunya/2023-09-21/las-farmacias-catalanas-distribuiran-productos-menstruales-gratuitos-a-partir-de-2024.html",
                 "img": "/media/news/farmacia.png"},
             2: {"title": "Como ayudar a tu hija a superar el miedo al uso del tampon y la copa menstrual",
                 "link": "https://elpais.com/mamas-papas/expertos/2023-08-28/como-ayudar-a-tu-hija-a-superar-el-miedo-al-uso-del-tampon-y-la-copa-menstrual.html",
                 "img": "/media/news/copa_menstrual.jpg"}}


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
        base = request.build_absolute_uri('/').rstrip('/')
        resolved = {}
        for k, v in news_dict.items():
            resolved[k] = {**v, 'img': base + v['img']}
        return Response({'news': resolved}, status=status.HTTP_200_OK)


class QuizApiView(APIView):

    def get(self, request):
        return Response({'message': "Quiz"}, status=status.HTTP_200_OK)


MOCK_PROMPT = (
    "¡Hola! Soy Draculine, tu asesora en temas de menstruación. Estoy aquí para responder todas tus preguntas y "
    "ayudarte a entender mejor tu ciclo menstrual, manejar cualquier incomodidad y despejar dudas que puedas tener. "
    "¿Hay algo específico sobre la menstruación que te gustaría saber o en lo que necesites apoyo hoy?"
)


def generate_bard_response(bard, message):
    if HAS_BARD:
        bard, new_message = bard_api.ask(bard, message)
        return bard, new_message
    return None, f"[Mock mode] Gràcies per la teva pregunta: «{message}». El chatbot real necessita l'API de Google Bard."


class ChatApiView(APIView):
    def get(self, request):
        if HAS_BARD:
            bard, prompt = bard_api.init()
            cache.set('bard-model', bard)
        else:
            prompt = MOCK_PROMPT

        messages_dict = {0: prompt}
        cache.set('messages-dict', messages_dict)
        return Response({'messages_dict': messages_dict, 'message': prompt}, status=status.HTTP_200_OK)

    def post(self, request):
        bard = cache.get('bard-model')
        messages_dict = cache.get('messages-dict') or {0: MOCK_PROMPT}
        message = request.data.get('message')

        messages_dict[len(messages_dict)] = message
        cache.set('messages-dict', messages_dict)

        if message:
            bard, response_message = generate_bard_response(bard, message)
            if bard:
                cache.set('bard-model', bard)
            messages_dict[len(messages_dict)] = response_message
            cache.set('messages-dict', messages_dict)
            return Response({'messages_dict': messages_dict, 'message': response_message}, status=201)
        else:
            return Response({'error': "Message not provided"}, status=400)


def base64_to_image(base64_string):
    # Decode the base64 string to bytes
    print(type(base64_string))
    image_bytes = base64.b64decode(base64_string)
    print(type(image_bytes))

    # Create a BytesIO object and load the image
    image_buffer = io.BytesIO(image_bytes)
    print(type(image_buffer))
    image = Image.open(image_buffer)
    print(type(image))

    return image


class CameraApiView(APIView):

    def get(self, request):
        return Response({'message': "Camera"}, status=status.HTTP_200_OK)

    def post(self, request):
        if not HAS_VISION:
            return Response({'image': 'Image received', 'ratio': '[Mock mode] Vision model not available'}, status=status.HTTP_200_OK)

        image_file = request.data['image']
        with open('updated.jpeg', 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        image = Image.open(image_file)
        image_rgb = image.convert('RGB')
        image_path, ratio = get_blood_ratio(image_rgb)
        return Response({'image': 'Image received', 'ratio': ratio}, status=status.HTTP_200_OK)


class MessagesApiView(APIView):

    def get(self, request):
        messages_dict = cache.get('messages-dict')
        return Response({'messages_dict': messages_dict}, status=status.HTTP_200_OK)
