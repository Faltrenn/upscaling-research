from keras import models, layers
from PIL import Image
import numpy as np


def create_model(input_shape) -> models.Sequential:
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Conv2D(64, (9, 9), activation="relu", padding="same"))
    model.add(layers.Conv2D(32, (1, 1), activation="relu", padding="same"))
    model.add(layers.Conv2D(3, (5, 5), activation="sigmoid", padding="same"))

    return model


def normalize_image(image: Image.Image) -> np.ndarray:
    return np.array(image).astype(np.float32) / 255.0


def open_normalized_image(filepath: str) -> np.ndarray:
    return normalize_image(Image.open(filepath).convert("RGB"))


def preprocess_image(file_path: str, scale: int) -> np.ndarray:
    image = Image.open(file_path).convert("RGB")

    w, h = image.size

    image = image.resize((w * scale, h * scale), Image.Resampling.BICUBIC)

    return normalize_image(image)
