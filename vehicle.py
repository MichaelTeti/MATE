from Components.joystick_controller import *
from Components.camera import *
from Components.object_detector import *

import cv2
import os
import numpy as np


class Vehicle:
    def __init__(self, controller='joystick', motor_fps=10, cam_fps=10, collect_data=False,
                 data_save_path=None, model_config_path=None, model_weights_path=None, img_size=256):
        self.camera = Camera(fps=cam_fps, img_size=img_size)
        self.object_model = ObjectDetector(model_config_path, model_weights_path)
        self.controller = JoystickController(check_freq=motor_fps)
        self.collect_data = collect_data
        self.data_save_path = data_save_path
        self.image_save_path = os.path.join(self.data_save_path, 'Images')
        self.check_data_path()
        self.run()


    def check_data_path(self):
        if self.collect_data:
            assert(self.data_save_path is not None), 'data_save_path must not be None if collect_data is True'
            if not os.path.isdir(self.data_save_path): os.mkdir(self.data_save_path)
            if not os.path.isdir(self.image_save_path): os.mkdir(self.image_save_path)


    def run(self):
        while not self.controller.shutdown:
            self.controller.update_motors()
            frame = self.camera.capture()
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
            detections = self.object_model.detect(frame)
            print(detections)

