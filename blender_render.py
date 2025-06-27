import os
from sys import argv, path

main_file_path = os.path.dirname(os.path.abspath(__file__))

path.append(main_file_path)

from utils import get_and_check_flags


def error():
    print("USAGE")
    print(
        f"blender --background --python {argv[0]} -- -f files.blend ... -r widthxheight ..."
    )
    quit(0)


try:
    import bpy  # type: ignore
except:
    error()

output_dir = os.path.join(main_file_path, "images")


def render(model: str, width: int, height: int):
    model_file_name = ".".join(os.path.basename(model).split(".")[:-1])
    file_output = f"{model_file_name}_{width}x{height}.png"
    path_output = os.path.join(output_dir, file_output)

    bpy.context.scene.render.resolution_x = width
    bpy.context.scene.render.resolution_y = height
    bpy.context.scene.render.filepath = path_output

    bpy.ops.render.render(write_still=True)


flags = get_and_check_flags(argv, ("-f", "-r"))

models = flags["-f"]
print(models)

resolutions = []
for res in flags["-r"]:
    splitted = res.split("x")
    resolutions.append([int(splitted[0]), int(splitted[1])])

print(resolutions)
print(models)

for model in models:
    print(f"Starting {model}")
    bpy.ops.wm.open_mainfile(filepath=model)

    for width, height in resolutions:
        render(model, width, height)
        print(f"Done {model} {width}x{height}")
