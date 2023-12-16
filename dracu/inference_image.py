from roboflow import Roboflow
import numpy as np
from PIL import Image


def predict_image(image: Image):
    image_name = 'updated.jpeg'
    image.save(image_name)

    rf = Roboflow(api_key="vf5yU2ElW0lYh48sa06D")
    project = rf.workspace().project("femenine-hygiene")
    model = project.version(2).model
    solution = model.predict(image_name)
    solution.save('prediction.jpg')
    print(solution.json())


#if name == 'main':
#    test = Image.open('Telegram/photo1702757498.jpeg')
#    predict_image(test)