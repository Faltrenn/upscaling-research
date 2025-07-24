from PIL import Image
import os


IMAGES_PATH = "../images/"

def mirror_and_save(image_path: str):
    img = Image.open(image_path)

    img_mirrored_h = img.transpose(Image.FLIP_LEFT_RIGHT)
    img_mirrored_v = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_mirrored_hv = img_mirrored_h.transpose(Image.FLIP_TOP_BOTTOM)

    os.makedirs(IMAGES_PATH, exist_ok=True)

    basename = os.path.basename(image_path)

    parts = basename.split("_")
    second_part = parts[-1]

    name = "_".join(parts[:-1])
    
    caminho_saida_mirrored_h = os.path.join(IMAGES_PATH, f"{name}_mirrored_h_{second_part}")
    caminho_saida_mirrored_v = os.path.join(IMAGES_PATH, f"{name}_mirrored_v_{second_part}")
    caminho_saida_mirrored_hv = os.path.join(IMAGES_PATH, f"{name}_mirrored_hv_{second_part}")

    img_mirrored_h.save(caminho_saida_mirrored_h)
    img_mirrored_v.save(caminho_saida_mirrored_v)
    img_mirrored_hv.save(caminho_saida_mirrored_hv)

    print(os.path.basename(caminho_saida_mirrored_h))
    print(os.path.basename(caminho_saida_mirrored_v))
    print(os.path.basename(caminho_saida_mirrored_hv))

IMAGES_IN_PATH = sorted(
        [IMAGES_PATH + file for file in os.listdir(IMAGES_PATH) if file.endswith(".png")]
    )

for image in IMAGES_IN_PATH:
    mirror_and_save(IMAGES_PATH + image)