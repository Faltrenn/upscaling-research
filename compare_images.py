from sys import argv
from PIL import Image


if len(argv) < 3:
    print("USAGE")
    print(f"python3 {argv[0]} file1 file2")
    quit(1)

file_path1, file_path2 = argv[1], argv[2]
file1 = Image.open(file_path1)
file2 = Image.open(file_path2)

if file1.size != file2.size:
    print("Images doesnt have same dimensions!")
    print(f"{file_path1} - {file1.size}\n{file_path2} - {file2.size}")
    quit(1)

width, height = file1.size

pixels1 = file1.load()
pixels2 = file2.load()

if not (pixels1 and pixels2):
    print("Some error reading pixels")
    quit(0)

error_avr = 0

for i in range(width):
    for j in range(height):
        for k in range(3):
            error_avr += abs(pixels1[i, j][k] - pixels2[i, j][k])

error_avr /= width * height * 3

error_percentage = error_avr * 100 / 255

print(f"Error percentage {error_percentage}%")
