from bardapi import BardCookies


def init():
    cookie_dict = {
        "__Secure-1PSID": "dwj5EheYAc7k5Iczm377qGm5DpLptdP7guY17AFHYHXS2Fzg4pYipp1xnl0pmny0awIisA.",
        "__Secure-1PSIDTS": "sidts-CjEBPVxjSkDk38tDRV_ZyJkffp9PVddVqPcOv0z1BJK8QKJxO53pGc86xHEfF6XFbxgGEAA",
        "__Secure-1PSIDCC": "ABTWhQGGI57NMpdYH0fLG6lFNDhp6YfTS0bYZ_q536wkue84fkSAqKdso-Y2N0IpQtVTle67S8A"
    }

    #cookie_dict = get_cookie_dict()  # cookies_dict

    bard = BardCookies(cookie_dict=cookie_dict)

    # Program AI
    response = bard.get_answer(
        "Eres una IA programada para actuar como una educadora sexual especializada en menstruación, con un enfoque "
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
