import serial
import pygame
import time
import os


class JoystickController:
    def __init__(self, check_freq=10, serial_port='/dev/ttyACM0'):
        pygame.init()
        self.j = pygame.joystick.Joystick(0)
        self.j.init()

        port_parent, port_child = os.path.split(serial_port)
        assert(port_child in os.listdir(port_parent)), \
            'Serial port {} not found. Please make sure it exists.'.format(port_child)
        self.ser = serial.Serial(serial_port, 115200)
   
        self.axes = [1, 3]
        self.check_interval = 1.0 / check_freq
        self.last_check = self.check_interval
        self.shutdown = False
        self.serial_output = None
        self.collect_data = False


    def update_motors(self):
        pygame.event.pump()
        if self.j.get_button(13) == 1:
            self.shutdown = True
        elif self.j.get_button(15) == 1:
            if not self.collect_data: self.collect_data = True
            elif self.collect_data: self.collect_data = False

        if time.time() - self.last_check >= self.check_interval:
            recent_values = []

            for current_axis in self.axes:
                latest_value = self.j.get_axis(current_axis)
                latest_value = ((latest_value + 1.0) / 2.0) * 100  # turn the values to integers in the range [0, 100]
                value_mod = str(int(latest_value))
                recent_values.append(value_mod)

            self.serial_output =','.join(recent_values) + ';' 
            self.serial_output = self.serial_output + str(int(self.collect_data)) + '.'

            self.ser.write(self.serial_output.encode())
            self.last_check = time.time()
