import paho.mqtt.client as mqtt
from djitellopy import Tello, TelloSwarm
from time import sleep
import base64
import time
import cv2
import threading
import numpy as np





def on_message(cli, userdata, message):
    global sending_video
    global client

    print(message.topic)
    message.payload = message.payload.decode("utf-8")
    # print(message.payload)

    if message.topic == 'ConnectSwarm':
        client.subscribe('takeoff')
        client.subscribe('land')
        client.subscribe('forward')
        client.subscribe('left')
        client.subscribe('Flip')
        client.subscribe('BasicLines')
        client.subscribe('estabilidad')
        client.subscribe('right')
        client.subscribe('back')
        client.subscribe('stop')
        client.subscribe('up')
        client.subscribe('down')
        client.subscribe('TRight')
        client.subscribe('TLeft')
        client.subscribe('state')
        client.subscribe('StartVideoStream')

        '''for i, tello in zip(range(2), telloswarm):
            tello.LOGGER.setLevel(logging.ERROR)
            tello.connect()
            print(f'Tello Battery {i + 1}: {tello.get_battery()}')
            tello.change_vs_udp(8881 + i)
            tello.set_video_resolution(Tello.RESOLUTION_480P)
            tello.set_video_bitrate(Tello.BITRATE_1MBPS)'''
        tello1.connect()
        tello1.change_vs_udp(8881)
        tello1.set_video_resolution(Tello.RESOLUTION_480P)
        tello1.set_video_bitrate(Tello.BITRATE_1MBPS)
        #tello1.set_video_fps(Tello.FPS_30)


        tello2.connect()
        tello2.change_vs_udp(8882)
        tello2.set_video_resolution(Tello.RESOLUTION_480P)
        tello2.set_video_bitrate(Tello.BITRATE_1MBPS)
        #tello2.set_video_fps(Tello.FPS_30)

        tello3.connect()
        tello3.change_vs_udp(8883)
        tello3.set_video_resolution(Tello.RESOLUTION_480P)
        tello3.set_video_bitrate(Tello.BITRATE_1MBPS)


        '''tello4.connect()
        tello4.change_vs_udp(8884)
        tello4.set_video_resolution(Tello.RESOLUTION_480P)
        tello4.set_video_bitrate(Tello.BITRATE_1MBPS)

'''
        swarm.connect()
        client.publish('connectedSwarm', 'ok')
        print(f'Tello1 Battery : {tello1.get_battery()}')
        #print(f'Tello2 Battery : {tello2.get_battery()}')
        update = False
        battery1 = tello1.get_battery()
       # battery2 = tello2.get_battery()

        threading.Thread(target=lambda: update_indicators()).start()
        #for tello in swarm:
         #   print(f'Tello1 Battery : {swarm.get_battery(0)}')
    flip = True
    fly = True

    if message.topic == 'takeoff':
        swarm.takeoff()

    elif message.topic == 'land':
        swarm.land()

    elif message.topic == 'forward':
        if message.payload == '0':
            move_drones(message.topic)
        else:
            move_one_drone(message.topic, message.payload)
    elif message.topic == 'left':
        if message.payload == '0':
            move_drones(message.topic)
        else:
            move_one_drone(message.topic, message.payload)
    elif message.topic == 'right':
        if message.payload == '0':
            move_drones(message.topic)
        else:
            move_one_drone(message.topic, message.payload)

    elif message.topic == 'back':
        # swarm.send_rc_control(0, -30, 0, 0)
        print('BACK')

    elif message.topic == 'stop':
        swarm.send_rc_control(0, 0, 0, 0)
    elif message.topic == 'up':
        swarm.send_rc_control(0, 0, 30, 0)
    elif message.topic == 'down':
        swarm.send_rc_control(0, 0, -30, 0)
    elif message.topic == 'TRight':
        swarm.send_rc_control(0, 0, 0, -50)
    elif message.topic == 'TLeft':
        swarm.send_rc_control(0, 0, 0, 50)
    elif message.topic == 'StartVideoStream':
        client.subscribe('StopVideoStream')
        tello1.streamon()
        tello1_video = threading.Thread(target=tello_video, args=(tello1, 1), daemon=True)
        tello1_video.start()

        '''tello2.streamon()
        tello2_video = threading.Thread(target=tello_video, args=(tello2, 2), daemon=True)
        tello2_video.start()'''

        '''tello3.streamon()
        tello3_video = threading.Thread(target=tello_video, args=(tello3, 3), daemon=True)
        tello3_video.start()'''

        '''tello4.streamon()
        tello4_video = threading.Thread(target=tello_video, args=(tello4, 4), daemon=True)
        tello4_video.start()'''

        '''tello5.streamon()
        tello5_video = threading.Thread(target=tello_video, args=(tello2, 2), daemon=True)
        tello5_video.start()'''

    elif message.topic == 'StopVideoStream':
        sending_video = False
    elif message.topic == 'Flip':
         if flip:
             tello1_fpath = ['f']
             tello2_fpath = ['f']


             for i in range(2):
                 flip1 = tello1_fpath[i]
                 flip2 = tello2_fpath[i]

                 tello1_flip = threading.Thread(target=tello_flip, args=(tello1, flip1), daemon=True)
                 tello2_flip = threading.Thread(target=tello_flip, args=(tello2, flip2), daemon=True)

                 tello1_flip.start()
                 tello2_flip.start()

                 tello1_flip.join()
                 tello2_flip.join()
    elif message.topic == 'BasicLines':
        #tello_simplelines()
        tello_waving()
    elif message.topic == 'estabilidad':
        #tello_simplelines()
        show_mode()



landed =False
video = False
def move_drones(direction):
    directions.pop()
    directions.insert(0, direction)
    print(directions)
    for i, tello in zip(directions, swarm):
        if i == 'left':
            tello.rotate_counter_clockwise(90)
        elif i == 'right':
            tello.rotate_clockwise(90)
        # tello.move_forward(50)

    swarm.move_forward(50)


'''def tello_video(tello, drone_number):
    telloswarm.parallel(lambda drone, tello: tello.streamon())
    time.sleep(3)

    tello1_video = threading.Thread(target=tello_video, args=(telloswarm.tellos[0], 1), daemon=True)
    tello2_video = threading.Thread(target=tello_video, args=(telloswarm.tellos[1], 2), daemon=True)
    #tello3_video = threading.Thread(target=tello_video, args=(telloswarm.tellos[2], 3), daemon=True)
    tello1_video.start()
    tello2_video.start()
    #tello3_video.start()

    frame1 = tello1.get_frame_read().frame
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    cv2.imshow(f'Tello {1}', frame1)

    frame2 = tello2.get_frame_read().frame
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    cv2.imshow(f'Tello {2}', frame2)

    #frame3 = tello3.get_frame_read().frame
    #frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
    #cv2.imshow(f'Tello {3}', frame3)

    #tello3.set_video_fps(Tello.FPS_30)
    while not landed:

        frame = tello.get_frame_read().frame


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow(f'Tello {drone_number}', frame)
        cv2.moveWindow(f'Tello {drone_number}', (drone_number - 1) * 900, 50)

        if cv2.waitKey(40) & 0xFF == ord('q'):
            cv2.destroyWindow(f'Tello {drone_number}')
            break
'''


def tello_video(tello, drone_number):
    while not landed:

        frame = tello.get_frame_read().frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow(f'Tello {drone_number}', frame)
        cv2.moveWindow(f'Tello {drone_number}', (drone_number - 1) * 900, 50)
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break


if video:
    telloswarm.parallel(lambda drone, tello: tello.streamon())
    time.sleep(3)

    tello1_video = threading.Thread(target=tello_video, args=(telloswarm.tellos[0], 1), daemon=True)
    tello2_video = threading.Thread(target=tello_video, args=(telloswarm.tellos[1], 2), daemon=True)
    #tello3_video = threading.Thread(target=tello_video, args=(telloswarm.tellos[2], 3), daemon=True)
    tello1_video.start()
    tello2_video.start()
    #tello3_video.start()'''
def move_one_drone(dir, drone_id):
    for i, tello in enumerate(swarm):
        if str(i+1) == drone_id:
            tello.move(dir, 20)
def tello_flip(tello, direction):
    tello.flip(direction)

def tello_simplelines():
    tello1.send_rc_control(0,0,30,0)
    tello2.send_rc_control(0, 10, 0, 0)
    sleep(5)
    tello1.send_rc_control(0, 0, -30, 0)
    tello2.send_rc_control(0, -10, 0, 0)

def puntos_sinusoide(x1, x2, frecuencia=1, fase=0):
    """
    Genera los valores de y para dos puntos que siguen el movimiento de una sinusoide.

    Argumentos:
        x1 (float): Valor de x para el primer punto.
        x2 (float): Valor de x para el segundo punto.
        frecuencia (float, opcional): Frecuencia de la sinusoide.
        fase (float, opcional): Fase de la sinusoide.

    Retorna:
        tuple: Tupla de dos valores de y correspondientes a los puntos en x1 y x2.
    """
    y1 = np.sin(frecuencia * x1 + fase) + 4.5  # Desplazar hacia arriba para que esté centrada
    y2 = np.sin(frecuencia * x2 + fase) + 4.5  # Desplazar hacia arriba para que esté centrada
    return y1, y2
def show_mode():
    #Show para 4 DRONES
    #telloswarm.move_up(50)
    '''telloswarm.takeoff()
    path_1 = [(216, 0, 130, 70, 1), (216, 0, 130, 70, 2), (216, 0, 130, 70, 3), (216, 0, 130, 70, 4)]
    path_2 = [(216, 0, 130, 70, 2), (216, 0, 130, 70, 3), (216, 0, 130, 70, 4), (90, 0, 130, 70, 5)]
    path_3 = [(216, 0, 130, 70, 3), (216, 0, 130, 70, 4), (90, 0, 130, 70, 5), (90, 0, 130, 70, 6)]
    path_4 = [(216, 0, 130, 70, 4), (90, 0, 130, 70, 5), (90, 0, 130, 70, 6), (90, 0, 130, 70, 7)]
    tello_waving()
    tello1.enable_mission_pads()
    tello2.enable_mission_pads()
    tello3.enable_mission_pads()
    tello4.enable_mission_pads()
    telloswarm.parallel(
        lambda drone, tello: tello.go_xyz_speed_mid(path_1[drone][0], path_1[drone][1], path_1[drone][2],
                                                    path_1[drone][3], path_1[drone][4]))
    telloswarm.parallel(
        lambda drone, tello: tello.go_xyz_speed_mid(path_2[drone][0], path_2[drone][1], path_2[drone][2],
                                                    path_2[drone][3], path_2[drone][4]))
    telloswarm.parallel(
        lambda drone, tello: tello.go_xyz_speed_mid(path_3[drone][0], path_3[drone][1], path_3[drone][2],
                                                    path_3[drone][3], path_3[drone][4]))
    telloswarm.parallel(
        lambda drone, tello: tello.go_xyz_speed_mid(path_4[drone][0], path_4[drone][1], path_4[drone][2],
                                                    path_4[drone][3], path_4[drone][4]))
'''
    telloswarm.takeoff()
    path_1 = [(270, 0, 144, 50, 1), (250, 0, 144, 40, 2), (310, 0, 144, 40, 3)]
    path_2 = [(260, 0, 144, 40, 2), (310, 0, 144, 40, 3), (135, 0, 144, 40, 4)]
    path_3 = [(310, 0, 144, 40, 3), (135, 0, 144, 40, 4), (81, 0, 144, 40, 5)]
    path_4 = [(135, 0, 144, 40, 4), (81, 144, 40, 5), (125, 0, 144, 40, 6)]
    #tello_waving()
    tello1.enable_mission_pads()
    tello2.enable_mission_pads()
    tello3.enable_mission_pads()
    tello4.enable_mission_pads()
    telloswarm.parallel(
        lambda drone, tello: tello.go_xyz_speed_mid(path_1[drone][0], path_1[drone][1], path_1[drone][2],
                                                    path_1[drone][3], path_1[drone][4]))
    telloswarm.parallel(
        lambda drone, tello: tello.go_xyz_speed_mid(path_2[drone][0], path_2[drone][1], path_2[drone][2],
                                                    path_2[drone][3], path_2[drone][4]))
    telloswarm.parallel(
        lambda drone, tello: tello.go_xyz_speed_mid(path_3[drone][0], path_3[drone][1], path_3[drone][2],
                                                    path_3[drone][3], path_3[drone][4]))
    telloswarm.parallel(
        lambda drone, tello: tello.go_xyz_speed_mid(path_4[drone][0], path_4[drone][1], path_4[drone][2],
                                                    path_4[drone][3], path_4[drone][4]))

    sleep(50)

    tello_waving()

    sleep(5)
    swarm.land()
def tello_waving():
    '''telloswarm.tellos[0].speed = 100
    telloswarm.move_up(20)
    sleep(10)
    telloswarm.tellos[0].send_rc_control(0, 0, 20, 0
    sleep(10)
    telloswarm.tellos[0].send_rc_control(0, 0, -20, 0)
    sleep(10)
    telloswarm.tellos[0].send_rc_control(0, 0, 20, 0)
    i = 0
    j = 1
    telloswarm.sync()
    telloswarm.parallel(lambda i, tello:telloswarm.send_rc_control(0, 0, 20 , 0))
    telloswarm.parallel(lambda j, tello: telloswarm.send_rc_control(0, 0, 20, 0))
    sleep(10)
    telloswarm.parallel(lambda i, tello: telloswarm.tellos[0].send_rc_control(0, 0, -20 , 0))
    telloswarm.parallel(lambda i, tello: telloswarm.tellos[1].send_rc_control(0, 0, 20, 0))
    sleep(10)
    telloswarm.parallel(lambda i, tello: telloswarm.tellos[0].send_rc_control(0, 0, 20 , 0))
    telloswarm.parallel(lambda i, tello: telloswarm.tellos[1].send_rc_control(0, 0, -20, 0))'''
    '''telloswarm.move_up(50)
    path_1 = [(0, 0, -40, 30, 3), (0, 0, 50, 30, 8)]
    path_2 = [(0, 0, -20, 30, 3), (0, 0, -30, 30, 8)]
    #path_3 = [(0, 120, 150, 40, 3), (-60, -60, 50, 20, 1), (60, -60, 100, 30, 2)]
    #path_4 = [(0, 0, 50, 20, 1), (0, 0, 50, 20, 2), (0, 0, 50, 20, 3)]
    telloswarm.parallel(lambda drone, tello: tello.enable_mission_pads)
    #telloswarm.parallel(
   #     lambda drone, tello: tello.go_xyz_speed_mid(path_1[drone][0], path_1[drone][1]))
    #telloswarm.parallel(
     #   lambda drone, tello: tello.go_xyz_speed_mid(path_2[drone][0], path_2[drone][1]))
    telloswarm.parallel(lambda drone, tello: tello.go_xyz_speed_mid(path_1[drone][0], path_1[drone][1], path_1[drone][2], path_1[drone][3], path_1[drone][4]))
    telloswarm.parallel(lambda drone, tello: tello.go_xyz_speed_mid(path_2[drone][0], path_2[drone][1], path_2[drone][2], path_2[drone][3], path_2[drone][4]))'''
    swarm.parallel(lambda drone, tello: tello.enable_mission_pads)

    drone1_wave_motion = [
          #  ascender
        (0, 0, -60, 0), (0, 0, 60, 0),(0, 0, -60, 0), (0, 0, 60, 0),(0, 0, -60, 0), (0, 0, 60, 0) #  descender
    ]
    drone2_wave_motion = [
          #  descender
        (0, 0, 60, 0),(0, 0, -60, 0),(0, 0, 60, 0),(0, 0, -60, 0),(0, 0, 60, 0),(0, 0, -60, 0)  #  ascender
    ]
    drone3_wave_motion = [
        #  ascender
        (0, 0, -40, 0), (0, 0, 40, 0), (0, 0, -40, 0), (0, 0, 40, 0), (0, 0, -40, 0), (0, 0, 40, 0)  # descender
    ]
    drone4_wave_motion = [
        #  descender
        (0, 0, 40, 0), (0, 0, -40, 0), (0, 0, 40, 0), (0, 0, -40, 0), (0, 0, 40, 0), (0, 0, -40, 0)  # ascender
    ]
    tello1.set_speed(70)
    tello2.set_speed(70)
    tello3.set_speed(70)
    tello4.set_speed(70)
    tello1.send_rc_control(0, 0, 30, 0)
    tello2.send_rc_control(0, 0, -30, 0)
    tello3.send_rc_control(0, 0, 20, 0)
    tello4.send_rc_control(0, 0, -20, 0)
    sleep(3)
    # Repetir el movimiento de la ola
    for _ in range(1):

        for motion1, motion2, motion3 in zip(drone1_wave_motion, drone2_wave_motion, drone3_wave_motion, drone4_wave_motion):
            tello1.send_rc_control(*motion1)
            tello2.send_rc_control(*motion2)
            tello3.send_rc_control(*motion3)
            tello4.send_rc_control(*motion4)
            time.sleep(2)
    #telloswarm.move_up(50)
    #telloswarm.send_rc_control(0, 0, 0, 20)
    #sleep(10)
    #telloswarm.land()

def update_indicators() -> None:
        """Se actualiza la baterua constantemente para cada drone."""
        update = True
        while update:
            #print("self.drone is true, updating indicators")
            battery1 = tello1.get_battery()

            battery2 = tello2.get_battery()
            battery3 = tello3.get_battery()
            battery4 = tello4.get_battery()
            client.publish('battery1', battery1)

            client.publish('battery2', battery2)
            client.publish('battery3', battery3)
            client.publish('battery4', battery4)
            #print(f"self.battery = {battery1}")
            time.sleep(1)

def tello_estabilidad():
    tello1.curve_xyz_speed(0, -25, 60, 0 ,-75, 60, 50)
def vuelta():
    tello1.go_xyz_speed(0, 60, 70, 100)
    tello2.go_xyz_speed(0, -60, 70, 100)
    sleep(5)
    tello1.go_xyz_speed(0, -60, -70, 100)
    tello2.go_xyz_speed(0, 60, -70, 100)

def NADA():
    """Activa los pads"""
    tello1.enable_mission_pads()
    tello2.enable_mission_pads()
    tello3.enable_mission_pads()
    tello4.enable_mission_pads()
    swarm.move_up(90)
    sleep(4)
    print("The tello mission pad t1 is:" + str(tello1.get_mission_pad_id()) )
    print("Y su altura es" + str(tello1.get_height()))
    print("The tello mission pad t2 is:" + str(tello2.get_mission_pad_id()) + "Y su altura es" + str(tello2.get_height()))
    print("The tello mission pad t3 is:" + str(tello3.get_mission_pad_id()) + "Y su altura es" + str(tello3.get_height()))
    print("The tello mission pad t4 is:" + str(tello4.get_mission_pad_id()) + "Y su altura es" + str(tello4.get_height()))
    tello1.rotate_clockwise(90)
    tello3.rotate_clockwise(90)
    tello2.rotate_counter_clockwise(90)
    tello4.rotate_counter_clockwise(90)
    sleep(8)

    tello1.rotate_counter_clockwise(90)
    tello3.rotate_counter_clockwise(90)

    tello2.rotate_clockwise(90)
    tello4.rotate_clockwise(90)

    tello_waving()

def dummy_service():
    global client
    global cap
    # ws://broker.hivemq.com:8000/mqtt (ionic vue)
    broker_address = 'broker.hivemq.com'
    broker_port = 8000
    client = mqtt.Client("Dash", transport="websockets")
    client.on_message = on_message
    client.connect(broker_address, broker_port)
    client.subscribe('ConnectSwarm')
    print('Waiting connection')
    client.loop_forever()


# def get_possible_ips(self):
#     """
#     Gets all the possible IP addresses for subnets that the computer is a part of.
#     :return: List of IP addresses.
#     """
#     infos = self.get_subnets()
#     ips = SubnetInfo.flatten([info.get_ips() for info in infos])
#     ips = list(filter(lambda ip: ip.startswith('192.168.3.'), ips))cmd
#     return ips


if __name__ == '__main__':

    # Before to create the swarm, configurate the drone tello for AP mode ('DESKTOPJanMas', 'janmasmartinez')
    # tello = Tello()
    # tello.connect()
    # bat = tello.get_battery()
    # print('Battery: ', bat)
    # tello.connect_to_wifi('TP-Link_E10A', '73136620')

    # create the swarm with all the drones connected to the AP
    # macs = ['60:60:1F:5D:BD:4D', '60:60:1F:D3:E4:5E', '60:60:1F:DC:32:88']
    # IPs = []
    # out = subprocess.run(["arp", "-a"], check=True, capture_output=True, text=True).stdout
    # res = out.split('\n')
    # for w in res:
    #     if '60-60-1f-dc-32-88' in w or \
    #             '60-60-1f-fd-1b-ca' in w or \
    #             '60-60-1f-5d-bd-4d' in w:
    #         IPs.append(w.split()[0])
    # print(IPs)

    directions = ['forward', 'forward', 'forward']
    #IPs = ['192.168.0.101','192.168.0.103']
    #swarm = TelloSwarm.fromIps(IPs)
    #swarm = TelloSwarm.fromIps(['192.168.0.106','192.168.0.108','192.168.0.109'])
    #telloswarm =TelloSwarm.fromIps(['192.168.0.106','192.168.0.108','192.168.0.109'])
    #swarm = TelloSwarm.fromIps(['192.168.0.104','192.168.0.105','192.168.0.103','192.168.0.101'])
    #telloswarm = TelloSwarm.fromIps(['192.168.0.104','192.168.0.105','192.168.0.103','192.168.0.101'])
    #swarm = TelloSwarm.fromIps([ '192.168.0.104','192.168.0.103','192.168.0.101'])
    telloswarm = TelloSwarm.fromIps([ '192.168.0.104','192.168.0.103','192.168.0.101','192.168.0.102'])
    tello1 = telloswarm.tellos[0]
    tello2 = telloswarm.tellos[1]
    tello3 = telloswarm.tellos[2]
    tello4 = telloswarm.tellos[3]
    #tello5 = telloswarm.tellos[4]
    #initiate the server
    dummy_service()

