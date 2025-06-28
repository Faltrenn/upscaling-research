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


def setup_gpu(device_type: str):
    cycles_prefs = bpy.context.preferences.addons["cycles"].preferences
    cycles_prefs.compute_device_type = device_type
    cycles_prefs.refresh_devices()

    for d in cycles_prefs.devices:
        d.use = True

    bpy.context.scene.cycles.device = "GPU"


def render(model: str, width: int, height: int, device_type: str = ""):
    model_file_name = ".".join(os.path.basename(model).split(".")[:-1])
    file_output = f"{model_file_name}_{width}x{height}.png"
    path_output = os.path.join(output_dir, file_output)

    if device_type:
        setup_gpu(device_type.upper())

    bpy.context.scene.render.resolution_x = width
    bpy.context.scene.render.resolution_y = height
    bpy.context.scene.render.filepath = path_output
    bpy.context.scene.render.image_settings.file_format = "PNG"

    bpy.ops.render.render(write_still=True)


flags = get_and_check_flags(argv, ("-f", "-r"), error)

models = flags["-f"]

resolutions = []
for res in flags["-r"]:
    splitted = res.split("x")
    resolutions.append([int(splitted[0]), int(splitted[1])])

for model in models:
    print(f"Starting {model}")
    bpy.ops.wm.open_mainfile(filepath=model)

    for width, height in resolutions:
        device_type = flags.get("-dtype", [""])[0]
        render(model, width, height, device_type)
        print(f"Done {model} {width}x{height}")
