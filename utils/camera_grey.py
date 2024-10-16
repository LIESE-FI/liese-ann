import cv2
import time

class VideoCaptureApp:
    def __init__(self, width=400, height=400, threshold=225, delay=1):
        self.width = width
        self.height = height
        self.threshold = threshold
        self.delay = delay
        self.vid = cv2.VideoCapture(0)
        self.vid.set(3, self.width)
        self.vid.set(4, self.height)

    def process_frame(self, frame):
        """Convierte el cuadro en escala de grises, lo binariza y dibuja contornos"""
        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Binarizar la imagen
        _, binary = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY_INV)
        # Encontrar y dibujar contornos
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        processed_frame = cv2.drawContours(frame.copy(), contours, -1, (0, 255, 0), 2)
        return processed_frame

    def run(self):
        """Ejecuta la captura de video con detección de contornos en tiempo real"""
        while True:
            # time.sleep(self.delay)
            ret, frame = self.vid.read()
            if not ret:
                break
            # Procesar el cuadro y obtener la imagen con contornos
            processed_frame = self.process_frame(frame)
            # Mostrar el cuadro procesado
            cv2.imshow("Contornos en tiempo real", processed_frame)
            # Salir con la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.release_resources()

    def release_resources(self):
        """Libera el video y destruye todas las ventanas abiertas"""
        self.vid.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = VideoCaptureApp()
    app.run()
