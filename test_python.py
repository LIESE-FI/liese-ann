# Importamos librerías
import cv2 
import mediapipe as mp



mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

# Ruta de la imagen
#image_path = "C:\\cursos\\Python\\Proyecto_ANN\\Pre_Procesamiento\\IMAGENES\\mano_prueba1.jpg"
#image_path = "C:\\cursos\\Python\\Proyecto_ANN\\Pre_Procesamiento\\IMAGENES\\Prueba_Dos.jpg"
image_path = "C:\\cursos\\Python\\Proyecto_ANN\\Pre_Procesamiento\\IMAGENES\\Prueba_Tres.jpg"

# Cargamos la imagen
image = cv2.imread(image_path)

# Verificamos si la imagen se cargó correctamente
if image is None:
    print(f"Error: No se pudo cargar la imagen desde {image_path}")
    exit()

# Inicializamos el módulo de detección de manos
with mphands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:

    # Convertimos la imagen a RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Procesamos la imagen para detectar las manos
    results = hands.process(image_rgb)

    # Convertimos la imagen de vuelta a BGR para visualizarla correctamente en OpenCV
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # Dibujamos los landmarks si se detectaron manos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image_bgr,
                hand_landmarks,
                mphands.HAND_CONNECTIONS
            )

    # Mostrar la imagen resultante
    #cv2.imwrite('output_image.jpg', image_bgr)
    cv2.imshow('Handtracker', image_bgr)


    # Esperar a que el usuario presione una tecla para cerrar
    cv2.waitKey(0)



# Liberar ventanas
cv2.destroyAllWindows()
