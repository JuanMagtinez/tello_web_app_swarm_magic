import cv2
from time import time, sleep
import torch
import pathlib
from djitellopy import Tello


def process_frame(model, frame, conf_threshold=0.6):
    # Conversion BGR a RGB para el modelo de "inference"
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Inference
    pred = model(frame_rgb)
    df = pred.pandas().xyxy[0]
    df = df[df["confidence"] > conf_threshold]

    # Inicializa el vector donde se pondrán los datos
    detected_objects = []

    for i in range(df.shape[0]):
        bbox = df.iloc[i][["xmin", "ymin", "xmax", "ymax"]].values.astype(int)
        name = df.iloc[i]["name"]
        confidence = df.iloc[i]["confidence"]

        # Añade los objetos detectados a la lista
        detected_objects.append(name)

        # Dibuja las bounding boxes en formato RGB 
        cv2.rectangle(frame_rgb, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)

        # Dibuja el texto de la etiqueta
        cv2.putText(frame_rgb,
                    f"{name}: {round(confidence, 2)}",
                    (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1)

    # Convierte a BGR para OpenCV 
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    return frame_bgr, detected_objects


def is_unique_objects(objects, count):
    """ Verifica si el conjunto de objetos contiene elementos únicos """
    return len(set(objects)) == count


def detect_cards(model, frame, conf_threshold=0.5, card_count=3):
    """ Detecta un número específico de cartas y verifica su unicidad """
    frame, detected_objects = process_frame(model, frame, conf_threshold)

    if len(detected_objects) == card_count and is_unique_objects(detected_objects, card_count):
        return detected_objects
    return None


if __name__ == '__main__':
    # Solución para el error "Error: cannot instantiate 'PosixPath' on your system" en Windows
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

    # Inicialización del dron Tello
    drone = Tello()
    drone.connect()
    drone.streamon()

    # Cargar el modelo (especificar tamaño de imagen para mejor detección)
    myModel = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
    myModel.conf = 0.25  # Ajustar umbral de confianza mínimo
    myModel.iou = 0.45  # Ajustar umbral de IoU para NMS (Non-Maximum Suppression)
    myModel.imgsz = 640  # Establecer tamaño de entrada

    previous = time()
    delta_min = 0.2  # Establecer intervalo mínimo de tiempo entre cuadros
    conf_threshold = 0.6  # Umbral de confianza para filtrado de detecciones

    detected_three_cards = None
    detected_two_cards = None
    stage = 1  # Fase del proceso: 1 = detección de 3 cartas, 2 = detección de 2 cartas

    
    try:
        while True:
            # Captura de cuadro por cuadro
            frame = drone.get_frame_read().frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            current = time()
            delta = current - previous

            if delta > delta_min:
                if stage == 1:
                    # Etapa de detección de tres cartas
                    detected_three_cards = detect_cards(myModel, frame, conf_threshold, card_count=3)

                    if detected_three_cards:
                        print(f"Las tres artas detectadas son: {detected_three_cards}")
                        # Esperar 10 segundos antes de continuar con la detección de dos cartas
                        sleep(10)
                        stage = 2  # Pasar a la etapa de detección de dos cartas
                        continue

                elif stage == 2:
                    # Etapa de detección de dos cartas
                    detected_two_cards = detect_cards(myModel, frame, conf_threshold, card_count=2)

                    if detected_two_cards:
                        print(f"Las cartas que siguen son: {detected_two_cards}")
                        three_card_set = set(detected_three_cards)
                        two_card_set = set(detected_two_cards)
                        missing_cards = list(three_card_set - two_card_set)

                        if missing_cards:
                            if missing_cards[0] == "9S":
                                drone.send_control_command(
                                    "EXT mled g 0bbbbbb00b0000b00b0000b00bbbbbb0000000b0000000b0000000b00bbbbbb0")
                                print(f"La carta escogida es: {missing_cards}")
                            if missing_cards[0] == "JC":
                                drone.send_control_command(
                                    "EXT mled g 0bbbbbbb00000b0000000b0000000b0000000b0000000b00b0000b00bbbbbb00")
                                print(f"La carta escogida es: {missing_cards}")
                            if missing_cards[0] == "2H":
                                drone.send_control_command(
                                    "EXT mled g bbbbbbbb0000000b0000000bbbbbbbbbb0000000b0000000b0000000bbbbbbbb")
                                print(f"La carta escogida es: {missing_cards}")
                        else:
                            print("Ninguana carta falta")

                        break  # Finalizar después de la detección final

            # Mostrar el cuadro resultante
            cv2.imshow('Drone Camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Al terminar, liberar recursos y cerrar la transmisión del dron
        cv2.destroyAllWindows()
        drone.streamoff()
        drone.end()
