import cv2
import mediapipe as mp

class HandTrackingApp:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5):
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.video_capture = cv2.VideoCapture(0)  # Iniciar captura de video desde la cámara

    def process_frame(self, frame):
        """Convierte el cuadro en RGB, procesa la detección de manos y dibuja los landmarks"""
        # Convertir el cuadro a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesar el cuadro para detectar manos
        with self.mp_hands.Hands(static_image_mode=False,
                                 max_num_hands=self.max_num_hands,
                                 min_detection_confidence=self.min_detection_confidence) as hands:
            results = hands.process(frame_rgb)

            # Dibujar landmarks si se detectaron manos
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )
        return frame

    def run(self):
        """Ejecuta la captura de video y procesamiento de detección de manos en tiempo real"""
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                print("Error: No se pudo capturar el cuadro de video.")
                break
            
            # Procesar el cuadro y obtener la imagen con landmarks
            processed_frame = self.process_frame(frame)
            
            # Mostrar el cuadro procesado
            cv2.imshow("Hand Tracking en tiempo real", processed_frame)
            
            # Salir con la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.release_resources()

    def release_resources(self):
        """Libera el video y destruye todas las ventanas abiertas"""
        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = HandTrackingApp()
    app.run()
