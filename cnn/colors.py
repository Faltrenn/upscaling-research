from PIL import Image
from sys import argv
import numpy as np

image_path = argv[1]

image = Image.open(image_path).convert("RGB")

print(np.asarray(image, np.uint8))


image.show()
