from roboflow import Roboflow
import numpy as np
from PIL import Image, ImageDraw
import cv2


def get_max(predictions):
    if len(predictions) < 1:
        return predictions
    else:
        dic = {}
        max = 0
        actualPred = None
        for pred in predictions['predictions']:
            if max < pred['confidence']:
                actualPred = pred
                max = pred['confidence']

        dic['predictions'] = actualPred
        return dic


def get_mask(image, prediction):
    # Create a blank mask image
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)

    # Draw the polygon on the mask
    polygon_points = [(point['x'], point['y']) for point in prediction['predictions']['points']]
    draw.polygon(polygon_points, fill=255)

    # Save or display the mask
    mask.save('binary_mask.png')  # Save the mask


def predict_image(image: Image):
    IMAGE_NAME = 'updated.jpeg'
    image.save(IMAGE_NAME)

    rf = Roboflow(api_key="vf5yU2ElW0lYh48sa06D")
    project = rf.workspace().project("femenine-hygiene")
    model = project.version(2).model
    solution = model.predict(IMAGE_NAME)
    solution.save('prediction.jpg')

    prediction = get_max(solution.json())

    get_mask(image, prediction)

    return blood_ratio(image)


def blood_ratio(image: Image):
    MASK_NAME = 'binary_mask.png'

    mask = cv2.imread(MASK_NAME, cv2.IMREAD_GRAYSCALE)
    mask3d = cv2.merge((mask, mask, mask))
    img = np.array(image)

    compresaLimpia = cv2.bitwise_and(img, mask3d)

    binarizada = cv2.inRange(compresaLimpia, (180, 0, 0), (255, 160, 160))
    _, binarizada = cv2.threshold(binarizada, 1, 255, cv2.THRESH_BINARY)

    areaCompresa = np.count_nonzero(mask == 255)
    areaSangre = np.count_nonzero(binarizada == 255)

    ratio = (areaSangre / areaCompresa) * 100

    return str(ratio)


def get_blood_ratio(image):
    """

    :param image:
    :return: The ratio and the cropped image
    """
    ratio = predict_image(image)

    image_path = 'prediction.jpg'

    return image_path, str(ratio)

