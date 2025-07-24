from keras import models, layers
from PIL import Image
import numpy as np
import tensorflow as tf
from keras.callbacks import EarlyStopping
import os


IMAGES_PATH = "../images/"

def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)


def create_model(input_shape, scale) -> models.Sequential:
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))

    model.add(layers.Conv2D(64, (9, 9), activation="relu", padding="same"))
    model.add(layers.Conv2D(32, (1, 1), activation="relu", padding="same"))

    model.add(layers.UpSampling2D(size=(scale, scale), interpolation="bilinear"))
    model.add(layers.Conv2D(input_shape[2], (5, 5), activation="relu", padding="same"))
    
    # channels = 3
    # model.add(layers.Conv2D(channels * scale * scale, (5, 5), activation="linear", padding="same", name='conv_before_shuffle'))
    # model.add(layers.Lambda(pixel_shuffle(scale), name='pixel_shuffle'))
    # model.add(layers.Conv2D(64, (9, 9), activation="relu", padding="same", name='refine_conv1'))
    # model.add(layers.Conv2D(channels, (1, 1), activation="linear", padding="same", name='final_conv_refined'))

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


def create_training_data(dataset: dict[str, list[str]], scale: int):
    X_train = []
    Y_train = []

    for input_image_name, output_images_names in dataset.items():
        input_image_path = IMAGES_PATH + input_image_name

        output_image_name = None
        if scale == 2:
            output_image_name = output_images_names[1]  # 640x480
        elif scale == 3:
            output_image_name = output_images_names[2]  # 960x720
        elif scale == 4:
            output_image_name = output_images_names[0]  # 1280x960

        if not output_image_name:
            continue

        output_image_path = IMAGES_PATH + output_image_name

        x = open_normalized_image(input_image_path)
        y = open_normalized_image(output_image_path)

        X_train.append(x)
        Y_train.append(y)

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    return X_train, Y_train


def predict(model_path:str, scale: int, input_path: str, output_filename: str):
    model_filename = os.path.basename(model_path)

    PREDICTS_MODEL_PATH = f"predicts/{model_filename[:-6]}/"
    os.makedirs(PREDICTS_MODEL_PATH, exist_ok=True)

    model = models.load_model(model_path)

    input_image = open_normalized_image(input_path)
    input_image = np.expand_dims(input_image, axis=0)

    print(f"Upscaling image {input_path} in {scale}x")

    predicted_image = np.squeeze(np.clip(model.predict(input_image) * 255, 0, 255))  # type: ignore
    predicted_image = predicted_image.astype(np.uint8)

    output_image = Image.fromarray(predicted_image).convert("RGB")
    output_image.save(PREDICTS_MODEL_PATH + output_filename)


def train(model_name:str, epochs: int, scale: int, patience: int = 50):
    IMAGES_IN_PATH = sorted(
        [file for file in os.listdir(IMAGES_PATH) if file.endswith(".png")]
    )

    images_names = list(set(["_".join(image.split("_")[:-1]) for image in IMAGES_IN_PATH]))

    dataset: dict[str, list[str]] = {}

    for image_name in images_names:
        input = f"{image_name}_320x240.png"
        dataset[input] = [
            image
            for image in IMAGES_IN_PATH
            if "_".join(image.split("_")[:-1]) == image_name and image != input
        ]

    early_stop = EarlyStopping(
        monitor="loss", patience=patience, restore_best_weights=True
    )

    X_train, Y_train = create_training_data(dataset, scale)
    srcnn_model = create_model(X_train.shape[1:], scale)
    srcnn_model.compile(optimizer="adam", loss="mean_squared_error")
    srcnn_model.fit(
        X_train, Y_train, epochs=epochs, batch_size=16, callbacks=[early_stop]
    )
    srcnn_model.save(f"models/{scale}x_{epochs}_{model_name}.keras")

    quit(0)