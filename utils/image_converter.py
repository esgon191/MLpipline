import numpy as np

def image_to_json(image): 
    """
    Принимает на вход объект image, отдает json-строку
    """

    image_data = np.array(np.expand_dims(np.array(image), axis=0))
    #image_data = json.dumps(image_data.tolist())
    image_data = image_data.tolist()


    return image_data