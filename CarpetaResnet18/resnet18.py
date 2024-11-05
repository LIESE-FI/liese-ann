# -*- coding: utf-8 -*-
"""Resnet18

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1M_iJLjeGII7DmLR0_BbMQwYcl_xugMjk

Instala pytorch
"""

pip install torch torchvision

from google.colab import drive
drive.mount('/content/drive')

#Creando subcarpetas para el entrenamiento
##una clase por letra

import os
import shutil

# Directorio de origen y destino
src_dir = '/content/drive/MyDrive/Colab Notebooks/train/images'  #  ruta a la carpeta de imágenes originales
dst_dir = '/content/dataset2/train'

# Crear la carpeta de destino si no existe
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# Mover imágenes a subcarpetas basadas en la letra (clase)
for img_file in os.listdir(src_dir):
    if img_file.endswith(('.jpg', '.jpeg', '.png')):  # Verificar extensiones de imagen
        # Extraer la letra de la clase del nombre del archivo (ej. 'A' de 'A0')
        class_label = img_file[0]  # La primera letra indica la clase

        # Crear la subcarpeta para la letra si no existe
        class_dir = os.path.join(dst_dir, class_label)
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)

        # Mover la imagen a la subcarpeta correspondiente
        shutil.move(os.path.join(src_dir, img_file), os.path.join(class_dir, img_file))

print("Reorganización completada. Las imágenes se han movido a subcarpetas por letra.")

import shutil
##Crear subcarpetas para las pruebas
src_dir = '/content/drive/MyDrive/Colab Notebooks/test/images'
dst_dir = '/content/dataset/test'

# Crear la carpeta de destino si no existe
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# Mover imágenes a subcarpetas basadas en la letra
for img_file in os.listdir(src_dir):
    if img_file.endswith(('.jpg', '.jpeg', '.png')):  # Verificar extensiones de imagen
        class_label = img_file[0]  # La primera letra indica la clase

        # Crear la subcarpeta para la letra si no existe
        class_dir = os.path.join(dst_dir, class_label)
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)

        # Mover la imagen a la subcarpeta correspondiente
        shutil.move(os.path.join(src_dir, img_file), os.path.join(class_dir, img_file))

print("Reorganización completada para el dataset de prueba.")

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# 1. Hiperparámetros
batch_size = 8
learning_rate = 0.001
num_epochs = 10

# 2. Transformaciones para el dataset
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 3. Cargar el Dataset
train_dataset = datasets.ImageFolder(root='/content/drive/MyDrive/Colab Notebooks/train/imagescarpetas', transform=transform)
test_dataset = datasets.ImageFolder(root='/content/drive/MyDrive/Colab Notebooks/valid/imagescarpe', transform=transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# 4. Definir la ResNet-18
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, len(train_dataset.classes))  # Ajustar para la detección de lenguaje de señas

# 5. Configuración de entrenamiento
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.00005)

# 6. Función de entrenamiento
def train(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    return running_loss / len(loader)

# 7. Función de validación
def validate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    return running_loss / len(loader), accuracy

# 8. Entrenamiento de la red
for epoch in range(num_epochs):
    train_loss = train(model, train_loader, criterion, optimizer, device)
    val_loss, val_accuracy = validate(model, test_loader, criterion, device)
    print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.4f}, '
          f'Validation Loss: {val_loss:.4f}, Accuracy: {val_accuracy:.2f}%')

# 9. Guardar el modelo entrenado
torch.save(model.state_dict(), 'modelo_resnet18_lenguaje_senas.pth')

import torch

# Cargar el modelo guardado
model_path = 'modelo_resnet18_lenguaje_senas.pth'
model.load_state_dict(torch.load(model_path))
model.eval()  # Cambiar a modo de evaluación

from PIL import Image
from torchvision import transforms

# Definir las transformaciones para la imagen de prueba
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Cargar y transformar una imagen de prueba
img_path = '//content/drive/MyDrive/PruebaResnet/Y_Bad.jpg'
#img_path ='/content/dataset2/test_sorted/D/D1_jpg.rf.89a5f6f41bf8bc795db94105f709dd34.jpg'
image = Image.open(img_path).convert('RGB')
image = transform(image)
image = image.unsqueeze(0)  # Añadir una dimensión para el batch

# Enviar la imagen al dispositivo (GPU o CPU)
image = image.to(device)

# Realizar la predicción
with torch.no_grad():
    output = model(image)
    _, predicted = torch.max(output, 1)

# Obtener la clase predicha
class_names = train_dataset.classes  # Nombres de las clases
predicted_class = class_names[predicted.item()]

print(f'Predicción: {predicted_class}')

!pip install onnx

pip install openvino

import torch
import torchvision.models as models
num_classes = 26

# Cargar el modelo ResNet-18 entrenado
model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load("modelo_resnet18_lenguaje_senas.pth"))
model.eval()

# Crear un tensor de entrada de ejemplo para la exportación
dummy_input = torch.randn(1, 3, 224, 224)  # batch_size=1, channels=3 (RGB), height=224, width=224

# Exportar a ONNX
torch.onnx.export(model, dummy_input, "modelo_resnet18.onnx", opset_version=11)

# Descargar e instalar OpenVINO
!pip install openvino-dev[onnx]

from openvino.tools.mo import convert_model

# Convertir el modelo ONNX a OpenVINO IR
convert_model("modelo_resnet18.onnx", output_dir="./openvino_model")

from openvino.runtime import serialize
from openvino.tools.mo import convert_model

# Ruta del modelo de entrada y carpeta de salida
input_model = "modelo_resnet18.onnx"
output_dir = "./openvino_model"

# Convertir el modelo y obtenerlo como objeto de OpenVINO
model = convert_model(input_model)

# Guardar el modelo en formato IR (.xml y .bin)
serialize(model, f"{output_dir}/modelo_resnet18.xml", f"{output_dir}/modelo_resnet18.bin")

print(f"Modelo convertido y guardado en: {output_dir}")