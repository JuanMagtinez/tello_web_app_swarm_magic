import paho.mqtt.client as mqtt
from djitellopy import Tello
import cv2 as cv

import base64
import time
import threading
import os

# initial position of our drone
x = 0
y = 0
z = 1
# create the boundaries
# notice that boundary is how long are each vector,
# so x_boundary = 3, means that last position of x vector will be 2
x_boundary = 4
y_boundary = 3
z_boundary = 4

def on_message(cli, userdata, message):
    global sending_video
    global client
    global user
    global x
    global y
    global z
    global x_boundary
    global y_boundary
    global z_boundary
    print(message.topic)

    if message.topic == 'Connect':


        client.subscribe('takeoff')
        client.subscribe('land')
        client.subscribe('forward')
        client.subscribe('left')
        client.subscribe('right')
        client.subscribe('back')
        client.subscribe('stop')
        client.subscribe('up')
        client.subscribe('down')
        client.subscribe('TRight')
        client.subscribe('TLeft')
        client.subscribe('state')
        client.subscribe('StartVideoStream')
        #client.subscribe('waiting2ndPly')
        client.publish('connected', user)
        tello.connect()

    elif message.topic == 'connected':


        tello.connect()


    elif message.topic == 'takeoff':
        tello.takeoff()
        client.publish('flyingState', 1)
    elif message.topic == 'land':
        tello.land()
        client.publish('flyingState', 0)

    elif message.topic == 'forward':
        if x == x_boundary - 1:
            client.publish('direction', 0)
        else:
            tello.move_forward(50)
            x = x + 1
            client.publish('direction', 1)

    elif message.topic == 'back':
        if x == 0:
            client.publish('direction', 0)
        else:
            tello.move_back(50)
            x = x - 1
            client.publish('direction', 1)

    elif message.topic == 'left':
        if y == 0:
            client.publish('direction', 0)
        else:
            tello.move_left(50)
            y = y - 1
            client.publish('direction', 1)

    elif message.topic == 'right':
        if y == y_boundary - 1:
            client.publish('direction', 0)
        else:
            tello.move_right(50)
            y = y + 1
            client.publish('direction', 1)

    elif message.topic == 'up':
        if z == z_boundary - 1:
            client.publish('direction', 0)
        else:
            tello.move_up(50)
            z = z + 1
            client.publish('direction', 1)

    elif message.topic == 'down':
        if z == 0:
            client.publish('direction', 0)
        else:
            tello.move_down(50)
            z = z - 1
            client.publish('direction', 1)

    elif message.topic == 'TRight':
        tello.rotate_clockwise(90)
        x, y = y, x_boundary - 1 - x
        y_boundary, x_boundary = x_boundary, y_boundary

    elif message.topic == 'TLeft':
        tello.rotate_counter_clockwise(90)
        x, y = y_boundary - 1 - y, x
        y_boundary, x_boundary = x_boundary, y_boundary

    elif message.topic == 'stop':
        tello.send_rc_control(0, 0, 0, 0)
    elif message.topic == 'state':
        bat = tello.get_battery()
        client.publish('battery', bat)
        print(bat)
        ##h = tello.get_height()
        ##client.publish('height', h)

    elif message.topic == 'StartVideoStream':
        client.subscribe('StopVideoStream')
        sending_video = True
        w = threading.Thread(target=send_video)
        w.start()
    elif message.topic == 'StopVideoStream':
        sending_video = False


def send_video():
    global sending_video
    global client

    tello.streamon()

    while sending_video:
        # Read Frame (not possible to get video stream in swarm mode)
        img = tello.get_frame_read().frame
        _, buffer = cv.imencode('.jpg', img)
        # # Converting into encoded bytes
        jpg_as_text = base64.b64encode(buffer)
        client.publish('videoFrame', jpg_as_text)
        # # Here we also want to send the video to the projector
        time.sleep(0.25)

        img = cv.resize(img, (720, 480))
        # Display the image into the screen
        cv.imshow("results", img)
        cv.waitKey(1)

#MAGIC DETECTOR


def dummy_service():
    global client
    global user
    user = 1
    # ws://broker.hivemq.com:8000/mqtt (ionic vue)
    broker_address = 'broker.hivemq.com'
    broker_port = 8000
    client = mqtt.Client("Dash", transport="websockets")
    client.on_message = on_message
    client.connect(broker_address, broker_port)
    client.subscribe('Connect')
    print('Waiting connection')
    client.loop_forever()


if __name__ == '__main__':
    tello = Tello()
    dummy_service()

