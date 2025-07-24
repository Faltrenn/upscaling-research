import os
from keras import models
from sys import argv
from keras import models

from model import (
    create_model,
    open_normalized_image,
    preprocess_image,
    IMAGES_PATH,
    train,
    predict,
)


def wrong_usage():
    print("WRONG USAGE!")
    print(f"{argv[0]} mode scale model_path/epochs input_path/model_name output_filename")
    print("scale can be 2, 3 or 4.")
    print("mode can be predict, predict_all and train.")
    print("in all cases, mode and scale are needed.")
    print("\tif train, epochs and model_name needs to be passed instead model_path and input_path respectively.")
    print("\t\tinput_path are ignored.")
    print("\tif predict, model_path, input_path and output_filename are needed.")
    print("\tif predict_all, just mode and scale are needed.")
    print("\t\tpredict_all predicts all low images in all trained models.")
    print("\t\tif model_path passed, predict all low images in passed model.")
    quit(1)


argc = len(argv)

if argc < 3:
    wrong_usage()

mode = argv[1]
scale = int(argv[2])

if (
    scale not in (2, 3, 4)
    or mode not in ("predict", "predict_all", "train")
    or (mode == "predict" and argc < 6)
):
    wrong_usage()

if mode == "train":
    if argc < 5:
        wrong_usage()

    epochs = int(argv[3])
    model_name = argv[4]
    train(model_name, epochs, scale)
    quit(0)

if mode == "predict":
    model_path = argv[3]
    input_path = argv[4]
    output_filename = argv[5]

    predict(model_path, scale, input_path,  output_filename)
    quit(0)

if mode == "predict_all":
    MODELS_PATH = "models/"
    models_paths = []
    if argc < 3:
        models_paths = sorted([
            MODELS_PATH + file
            for file in os.listdir(MODELS_PATH)
            if file.endswith(".keras") and file.startswith(f"{scale}x")
        ])
    else:
        models_paths = [argv[3]]

    LOW_IMAGES = sorted(
        [IMAGES_PATH + file for file in os.listdir(IMAGES_PATH) if "320x240" in file and not any(n in file for n in ("_h_", "_v_", "_hv_"))]
    )

    for model_path in models_paths:
        print(f"USING MODEL {model_path}")
        models.load_model(model_path).summary() # type: ignore
        
        for i, low_image in enumerate(LOW_IMAGES):
            predict(model_path, scale, low_image, f"{i}.png")
