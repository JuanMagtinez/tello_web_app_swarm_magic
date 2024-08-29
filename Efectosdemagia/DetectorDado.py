import cv2
from djitellopy import tello
from djitellopy import *
import  numpy as np
import time

CAMERA_FORWARD=1
CAMARA_DOWNWARD=0

'''
def send_expansion_command(self, expansion_cmd: str):
    """Sends a command to the ESP32 expansion board connected to a Tello Talent
    Use e.g. tello.send_expansion_command("led 255 0 0") to turn the top led red.
    """
    cmd = 'EXT {}'.format(expansion_cmd)
    self.send_control_command(cmd)
def run_bottom_video(drone):
    while True:
        frame = drone.get_frame_read().frame

        crop_img = frame[0:240, 0:320]
        cv2.imshow("crop img",crop_img)

        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

    cv2.destroyAllWindows()
    print('Finalizandoooo')
    drone.end()
    print("---Se temino el programa")




def main():
    # Inciamos el dron
    drone = tello.Tello()
    # Nos conectamos
    drone.connect()
    drone.set_video_direction(drone.CAMERA_DOWNWARD)

    drone.streamon()
    #drone.send_control_command("EXT mled g 000bb00000bb00000bb00000bbbbbbbbbbbbbbbb0bb0000000bb0000000bb000")
    #drone.send_control_command("EXT mled g bb0000bbbb0000bb00000000bb0000bbbb0000bb00000000bb0000bbbb0000bb")

    run_bottom_video(drone)


if __name__ == '__main__':
    main()
'''

def send_expansion_command(self, expansion_cmd: str):
    """Sends a command to the ESP32 expansion board connected to a Tello Talent
    Use e.g. tello.send_expansion_command("led 255 0 0") to turn the top led red.
    """
    cmd = 'EXT {}'.format(expansion_cmd)
    self.send_control_command(cmd)

def run_bottom_video(drone):
    while True:
        frame = drone.get_frame_read().frame
        if frame is None:
            continue

        crop_img = frame[0:240, 0:320]
        cv2.imshow("crop img", crop_img)

        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

        # Rango de colores para la máscara
        lower = np.array([0, 0, 0])
        upper = np.array([180, 255, 30])

        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(mask, kernel, iterations=2)
        erosion_dilate = cv2.dilate(erosion, kernel, iterations=3)

        cv2.imshow("mask", mask)
        cv2.imshow("erosion", erosion)
        cv2.imshow("erosion_dilate", erosion_dilate)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        res = cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 3)
        cv2.imshow("res", res)
        print("El número es:", len(contours))
        current_time = time.time()
        if len(contours) == 6:
            drone.send_control_command("EXT mled g bb0000bbbb0000bb00000000bb0000bbbb0000bb00000000bb0000bbbb0000bb")
        if len(contours) == 5:
            drone.send_control_command(
                    "EXT mled g bb0000bbbb0000bb00000bb000000bb00000000000000000bb0000bbbb0000bb")
            time.sleep(20)
        if len(contours) == 4:
            drone.send_control_command(
                    "EXT mled g bb0000bbbb0000bb00000000bb0000bbbb0000bb00000000bb0000bbbb0000bb")
            time.sleep(20)
        if len(contours) == 3:
            drone.send_control_command(
                    "EXT mled g bb000000bb00000000000bb000000bb00000000000000000000000bb000000bb")
            time.sleep(20)
        '''if current_time - last_command_time >= command_interval:'''
        if len(contours) == 2:
            drone.send_control_command(
                    "EXT mled g bb000000bb00000000000000000000000000000000000000000000bb000000bb")
            time.sleep(20)
        if len(contours) == 1:
            tello.send_control_command("EXT mled g b000000b0000000bb0000000000000000000000bb000000bb000000bbbbbbbbb")
            time.sleep(20)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    print('Finalizandoooo')
    drone.end()
    print("---Se terminó el programa")

def main():
    # Iniciamos el dron
    drone = Tello()
    # Nos conectamos
    drone.connect()
    drone.set_video_direction(drone.CAMERA_FORWARD)
    drone.streamon()

    run_bottom_video(drone)

if __name__ == "__main__":
    main()
