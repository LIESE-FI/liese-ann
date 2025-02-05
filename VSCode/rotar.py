#librerias a usar
import os
from PIL import Image
import matplotlib.pyplot as plt #para visualizar imagenes

#definicion de funcion para rotar imagen
def rotate_image(dir, angle, zoom=1):
  try:
    image = Image.open(dir)
    if zoom == 1:
      rotated_image = image.rotate(angle, expand=True)
      return rotated_image
    else:
      # Obtener el tamaño original de la imagen
      original_size = image.size
      #aplicar zoom a la imagen
      zoomed_image = image.resize((int(original_size[0] * zoom), int(original_size [1] * zoom)), Image.LANCZOS)
      #rotar la imagen
      rotated_image = zoomed_image.rotate(angle, expand=True)
      # Recortar la imagen al centro
      center_x, center_y = rotated_image.size[0] // 2, rotated_image.size[1] // 2
      left = center_x - original_size[0] // 2
      upper = center_y - original_size[1] // 2
      right = center_x + original_size[0] // 2
      lower = center_y + original_size[1] // 2
      cropped_image = rotated_image.crop((left, upper, right, lower))
      return cropped_image
  except Exception as e:
    print(f"Error al rotar la imagen: {e}")
    return None

#funcion para encontrar direccion de todos los archivos del dataset
def data_set_shift(dataset_dir):
  imagen_dir = []
  for folder_name in os.listdir(dataset_dir):
    folder_dir = os.path.join(dataset_dir, folder_name)
    for filename in os.listdir(folder_dir):
      full_dir = os.path.join(folder_dir, filename)
      if os.path.isfile(full_dir):
        imagen_dir.append(full_dir)
  return imagen_dir

# principal

#direccion de ejemplo

dir_dataset = r'C:\Users\jorge\Downloads\train\imagescarpetas'
angles = [-5,5,-10,10]

image_dataset_dir = data_set_shift(dir_dataset)

for filename in image_dataset_dir:
  if filename.endswith(('.jpg')):
      for angle in angles:
        rotated_image = rotate_image(filename, angle,zoom=1.2)

        newname = f"{os.path.splitext(filename)[0]}_rotada_{angle}{os.path.splitext(filename)[1]}"
        new_image_dir = os.path.join(dir_dataset, newname)

        rotated_image.save(new_image_dir)

