import os
from keras import callbacks, models
import numpy as np
from PIL import Image
from sys import argv


def wrong_usage():
    print("WRONG USAGE!")
    print(f"{argv[0]} mode scale model_path/epochs input_path outputh_path")
    print("scale can be 2, 3 or 4.")
    print("mode can be predict or train.")
    print("\tif train, epochs needs to be passed instead model_path.")
    print("\tinput_path are ignored.")
    print("\tif predict, model_path, input_path and output_path are needed.")
    quit(1)


argc = len(argv)

if argc < 3:
    wrong_usage()

mode = argv[1]
scale = int(argv[2])

if (
    scale not in (2, 3, 4)
    or mode not in ("predict", "train")
    or (mode == "predict" and argc < 6)
):
    wrong_usage()

# Import keras takes too long time, so, importing after check args.
from model import (
    create_model,
    open_normalized_image,
    preprocess_image,
)


IMAGES_PATH = "../images/"
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

        x = preprocess_image(input_image_path, scale=scale)
        y = open_normalized_image(output_image_path)

        X_train.append(x)
        Y_train.append(y)

    X_train = np.array(X_train)
    Y_train = np.array(Y_train)

    return X_train, Y_train


if mode == "train":
    from datetime import datetime
    from keras.callbacks import EarlyStopping

    def get_formatted_time() -> str:
        return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    epochs = int(argv[3])

    early_stop = EarlyStopping(
        monitor="val_loss", patience=15, restore_best_weights=True
    )

    X_train, Y_train = create_training_data(dataset, scale)
    srcnn_model = create_model(input_shape=X_train.shape[1:])
    srcnn_model.compile(optimizer="adam", loss="mean_squared_error")
    srcnn_model.fit(
        X_train, Y_train, epochs=epochs, batch_size=16, callbacks=[early_stop]
    )
    srcnn_model.save(f"models/{scale}x_{epochs}_{get_formatted_time()}.keras")

    quit(0)

model_path = argv[3]
input_path = argv[4]
output_path = argv[5]

model = models.load_model(model_path)

input_image = preprocess_image(input_path, scale=scale)
input_image = np.expand_dims(input_image, axis=0)

print(f"Upscaling image {input_path} in {scale}x")

predicted_image = np.squeeze(model.predict(input_image) * 255)  # type: ignore
predicted_image = predicted_image.astype(np.uint8)

output_image = Image.fromarray(predicted_image).convert("RGB")
output_image.show()
output_image.save(output_path)

Image.open(input_path).convert("RGB").show()
