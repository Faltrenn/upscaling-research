import os

models_dir = "cnn/models"

for filename in os.listdir(models_dir):
    if ":" in filename:
        new_filename = filename.replace(":", "-")
        old_path = os.path.join(models_dir, filename)
        new_path = os.path.join(models_dir, new_filename)

        try:
            os.rename(old_path, new_path)
            print(f"Renamed {filename} -> {new_filename}")
        except Exception as e:
            print(f"Erro ao renomear {filename}: {e}")
