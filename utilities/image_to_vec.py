import numpy as np
import os

from tensorflow import keras
from tensorflow.keras.applications import resnet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model

IMAGE_TARGET_SIZE = (224, 224)

class ImgageVectorizer(object):
    """Image Vectorizer class. Allows to extract embeddings from images by passing in the path. 

    It is based on the ResNet50 model trained on the ImageNet dataset. The output of the last average pool layer is provided 
    as the embedding vector. 
    """    
    def __init__(self):
        self.IMAGE_TARGET_SIZE = (224, 224)
        model = resnet50.ResNet50(weights='imagenet')
        self.embedding_model = Model(inputs=model.input, outputs=model.get_layer('avg_pool').output)


    def get_embedding(self, image_path):
        """Given an image path, the data cropped and processed according to ResNet50 specifications.

        Args:
            image_path (str): path-like string indicating location of the image in the file system.

        Returns:
            np.array: generated embedding
        """        
        image_vector = np.expand_dims(image.img_to_array(image.load_img(image_path, target_size=self.IMAGE_TARGET_SIZE)), axis=0)
        image_vector = resnet50.preprocess_input(image_vector)
        embedding_vector = self.embedding_model.predict(image_vector)
        return embedding_vector[0]


def get_embeddings_from_directory(dir_path, extension=".JPEG"):
    """Utility function to get embeddings using the ResNet50 model for an entire directory.
    Beware, it walks the given directory and subdirectories to look for images with a specific 
    extension.

    Args:
        dir_path (str): path-like string indicating the path to the directory in the file system.
        extension (str, optional): extension of images to look for. Defaults to ".JPEG".

    Returns:
        (np.array, list): numpy array with all generated embeddings and list with relative file paths to processed images.
    """    
    embedding_generator = ImgageVectorizer()

    image_paths = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(extension):
                image_paths.append(os.path.join(root, file))

    x = 0
    for i in image_paths:
        if x == 0:
            all_vectors = embedding_generator.get_embedding(i).reshape(1, -1)
        else:
            to_append = embedding_generator.get_embedding(i)
            to_append = to_append.reshape(1, -1)
            all_vectors = np.concatenate((all_vectors, to_append), axis=0)
        x += 1

    return all_vectors, image_paths

