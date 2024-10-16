#se importan las librerias 
import cv2
import matplotlib.pyplot as plt

# Ruta de la imagen en forma de variable 
#image_path = "C:\\cursos\\Python\\Proyecto_ANN\\Pre_Procesamiento\\IMAGENES\\mano_prueba1.jpg"
# image_path = "C:\\cursos\\Python\\Proyecto_ANN\\Pre_Procesamiento\\IMAGENES\\Prueba_Dos.jpg"
image_path = "C:\\cursos\\Python\\Proyecto_ANN\\Pre_Procesamiento\\IMAGENES\\Prueba_Tres.jpg"

#cargamos la imagen que vamos a trabajar 
imagen=cv2.imread(image_path)

#pasamos la imagen a formato RGB 
#se pasa a rgb ya que el formato de cv2 es por defecro RGB 
imagen = cv2.cvtColor(imagen,cv2.COLOR_BGR2RGB)

#POR LO TANTO CADA PIXEL SE ENCONTRARA COMPUESTA POR TRES VALORES
#(R,G,B), POR LO QUE EL SIGUIENTE PASO ES CONVERYIRLA A ESCALA GRISES 
gris = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)

#hacemos uso de imshow 
#mostamos imagen 
cv2.imshow("Imagen en gris", gris)

#para hacer el contorno  debemos generar una representación binaria 
# de la misma, en donde el valor de los pixeles de la misma sean, unicamente 0 (negro) 0 255 (blanco). 
#con cv2 threshold 
#A continuación pasaremos 2 valores (en este caso 225 y 255) mediante los cuales, estaremos indicando que 
# aquellos pixeles cuyo valor actual sea superior a 225, se le asigne como valor 255 (correspondiente al color blanco) 
# para convertir la imagen en binaria
#donde obendremos un array compuestto de 0 y 255
#se escoge el algoriton=mo THESH_Binaryb
_,binaria = cv2.threshold(gris,225,255,cv2.THRESH_BINARY_INV)

#mostrar imagen binaria 
plt.imshow(binaria, cmap="gray")
plt.axis('off')
plt.show



#detectamos contorno 
contronos,_ =cv2.findContours(binaria,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#dibuajamos contornos
imagen_final=cv2.drawContours(imagen,contronos,-1,(0,255,0),5)


plt.imshow(imagen_final)
plt.axis('off')
plt.show()

# Evitamos que la ventana se cierre inmediatamente
cv2.waitKey(0)

# Destruimos todas las ventanas abiertas
cv2.destroyAllWindows()

