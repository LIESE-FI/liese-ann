import cv2
import mediapipe as mp
import json
import time 
import os
from datetime import datetime

#funciones 
def load_config(filename="config.json"):
    try:
        with open(filename, "r") as file:
            datos = json.load(file)  # Cargar los datos desde el JSON
            return datos  # Retorna el diccionario con los valores
    except Exception as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return None


#--------------------------------------------------------------------
#--------------------------------------------------------------------
#---------------VARIABLES QUE HAY QUE INICIALIZAR--------------------
wait_flag = False
capture_flag = False
start_time = time.time()
color = (0,0,255)





#--------------------vARIABLES DE CAPTURA----------------------------
config = load_config("config.json") 

tiempo = int(config.get("tiempo", 0))
capturas = int(config.get("capturas", 0))
letra = config.get("letra", "")
carpeta = config.get("carpeta", "")
output_folder = f"{carpeta}/{letra}"
wait_time = int(config.get("tespera", 0))

total_capturas = tiempo * capturas
intervalo = 1/capturas
contador = total_capturas + 1

#-------------------impresion de configuracion-----------------------
print("------CONFIGURACION------")
print(f"Tespera: {wait_time} segundos")
print(f"Tiempo de captura: {tiempo} segundos")
print(f"Capturas por segundo: {capturas}")
print(f"Letra seleccionada: {letra}")
print(f"Carpeta destino: {output_folder}")


# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Capturar imagen desde la cámara web
cap = cv2.VideoCapture(0)

# Definir el margen (en píxeles)
margen = 50

# verificacion de la exitencia del folder al que se va a cargar los datos 
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la imagen a RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Procesar la imagen y detectar manos
    results = hands.process(image)

    # Convertir la imagen de vuelta a BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Dibujar el margen alrededor de la mano detectada
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtener las coordenadas del cuadro delimitador de la mano
            h, w, c = image.shape
            x_min = min([landmark.x for landmark in hand_landmarks.landmark]) * w
            y_min = min([landmark.y for landmark in hand_landmarks.landmark]) * h
            x_max = max([landmark.x for landmark in hand_landmarks.landmark]) * w
            y_max = max([landmark.y for landmark in hand_landmarks.landmark]) * h

            # Añadir margen
            x_min = max(0, int(x_min) - margen)
            y_min = max(0, int(y_min) - margen)
            x_max = min(w, int(x_max) + margen)
            y_max = min(h, int(y_max) + margen)
            
            roi = image[y_min:y_max, x_min:x_max]
            
            cv2.rectangle(image, (x_min-5 , y_min-5), (x_max+5, y_max+5), color, 2)
            # Dibujar el rectángulo con margen

    # Mostrar la imagen con el margen dibujado alrededor de la mano detectada
    if wait_flag == True:
        tiempo = time.time() - start_time 
        cv2.putText(image, f"Esperando...{wait_time-tiempo}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        print(f"Esperando...{5-tiempo}")
        if tiempo > wait_time:
            wait_flag = False
            capture_flag = True
            color = (0,255,0)
            print("Iniciando captura de imágenes.")
            contador = 0

    cv2.imshow('Hand Detection video', image)

    if contador < total_capturas:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_folder, f"{letra}{timestamp}{contador}.png")  # ✅ Corregido
        cv2.imwrite(filename, roi)  # Guarda la imagen
        print(f"imagen capturada en:{filename}")
        contador += 1
        time.sleep(intervalo)

    if contador >= total_capturas and capture_flag:  # ✅ Corregido
        capture_flag = False
        color = (0,0,255)  # Vuelve a rojo
        print("Fin de capturas")

    if cv2.waitKey(1) & 0xFF == ord('a'):
        start_time = time.time()
        print(f"Esperando {wait_time} segundos antes de iniciar la captura...")
        wait_flag = True
        color = (0,255,255)


    # Salir del bucle al presionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("adios")
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()