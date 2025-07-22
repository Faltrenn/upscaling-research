from sys import argv
from PIL import Image


if len(argv) < 3:
    print("USAGE")
    print(f"python3 {argv[0]} file1 file2")
    quit(1)

file_path, files_paths = argv[1], argv[2:]
file1 = Image.open(file_path)
files = [Image.open(file_path) for file_path in files_paths]

for file2 in files:
    if file1.size != file2.size:
        print("Images doesnt have same dimensions!")
        print(f"{file_path} - {file1.size}\n{file2.filename} - {file2.size}")
        quit(1)

width, height = file1.size

pixels1 = file1.load()

if not pixels1:
    print("Some error reading pixels")
    quit(0)

results = {}
bigger_filename_lenght = 0
for file2 in files:
    pixels2 = file2.load()

    if not pixels2:
        print(f"Some error reading pixels in {file2.filename}")
        continue

    error_avr = 0

    for i in range(width):
        for j in range(height):
            for k in range(3):
                error_avr += abs(pixels1[i, j][k] - pixels2[i, j][k])

    error_avr /= width * height * 3

    similarity_percentage = 100 - error_avr * 100 / 255

    results[file2.filename] = similarity_percentage

    if (bigger_filename_lenght := len(file2.filename)) > bigger_filename_lenght:
        bigger = bigger_filename_lenght


for filename, similarity_percentage in results.items():
    print(
        f"Similatiry percentage with {filename:<{bigger_filename_lenght}}: {similarity_percentage:.2f}%"
    )
