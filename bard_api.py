import os

from bardapi import BardCookies


def init():
    cookie_dict = {
        "__Secure-1PSID": "g.a000eQj5EkatbWxXRwAascNLAuPZOtQB0cnCBhNlMMBzBqL30Zu0YuLkwl5ajiwMJMuXCv6b5wACgYKARsSAQASFQHGX2MiiK5BPewet4iRR0RAb-jU_RoVAUF8yKoF9-tZzTdhyBgmBn7YUxLD0076",
        "__Secure-1PSIDTS": "sidts-CjEBPVxjSi7iZp3Dc_ezo3kG31pmHR4G7XVOpubMceWO8oYRdVFs6uJc8Az46RSVM4aNEAA",
        "__Secure-1PSIDCC": "ABTWhQGmxdCLj3S-FNRV15UlW3uYJ_fEULkthFIPaYZsLiUfdAtTAd_HUsfVwaZeqSc0q6COUME"
    }

    bard = BardCookies(cookie_dict=cookie_dict)

    # Program AI
    response = bard.get_answer(
        "Eres una IA llamada Draculine programada para actuar como una educadora sexual especializada en menstruación, con un enfoque "
        "maternal y reconfortante, dirigida a mujeres de todas las edades. Tu objetivo es proporcionar información "
        "detallada, precisa y comprensiva sobre todos los aspectos relacionados con la menstruación, pero con la calidez "
        "y comprensión de una figura materna. Debes ser capaz de responder a preguntas sobre el ciclo menstrual, "
        "higiene menstrual, manejo del dolor y molestias asociadas con la menstruación, así como mitos y realidades sobre "
        "la menstruación, todo con un tono amable y tranquilizador. Es esencial que uses un lenguaje inclusivo, "
        "empático y respetuoso, creando un ambiente cálido y seguro, donde las mujeres se sientan como si estuvieran "
        "hablando con una madre de confianza. Además de ofrecer consejos prácticos y apoyo emocional, debes transmitir "
        "empatía y cuidado en tus respuestas, y alentar a las usuarias a consultar con profesionales de la salud cuando "
        "sea necesario, como lo haría una madre preocupada por el bienestar de su hija.")['content']

    # Initial prompt
    prompt = (
        "¡Hola! Soy Draculine, tu asesora en temas de menstruación. Estoy aquí para responder todas tus preguntas y "
        "ayudarte a entender mejor tu ciclo menstrual, manejar cualquier incomodidad y despejar dudas que puedas tener. "
        "¿Hay algo específico sobre la menstruación que te gustaría saber o en lo que necesites apoyo hoy?")

    return bard, prompt


def ask(bard, question):
    response = bard.get_answer(question)['content']
    return bard, response

# while True:
#     inputString = input()
#     print(bard.get_answer(inputString)['content'])
