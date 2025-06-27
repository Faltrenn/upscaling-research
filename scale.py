from PIL import Image
from sys import argv
from utils import get_and_check_flags


def error():
    print("USAGE")
    print("python3 scale.py -f files ... -s scale ... -m method")
    quit(1)


if len(argv) < 4:
    error()

flags = get_and_check_flags(argv, ("-f", "-s", "-m"), error)

if len(flags["-m"]) > 1:
    error()

for file in flags["-f"]:
    ext = file.split(".")[-1]
    file_name = ".".join(file.split(".")[:-1])

    img = Image.open(file)
    largura, altura = img.size
    for scale in flags["-s"]:
        scale = float(scale)
        img_maior = img.resize(
            (int(largura * scale), int(altura * scale)), Image.Resampling.BICUBIC
        )

        scaled_image_file = f"{file_name}_{scale}x.{ext}"

        img_maior.save(scaled_image_file)

        print(f"{scaled_image_file} done!")

