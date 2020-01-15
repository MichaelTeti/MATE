from Components.joystick_controller import *
from Components.camera import *
from Models.data_collector import *
from Components.object_detector import *

import cv2
import os
import numpy as np


class Vehicle:
    def __init__(self, controller='joystick', motor_fps=10, cam_fps=10,
                 model_config_path=None, model_weights_path=None, img_size=256,
                 data_collection_interval=0.2):
        self.camera = Camera(fps=cam_fps, img_size=img_size)
        self.object_model = ObjectDetector(model_config_path, model_weights_path)
        self.controller = JoystickController(check_freq=motor_fps)
        self.data_collector = DataCollector(img_size=img_size, data_collection_interval=data_collection_interval)
        self.run()


    def run(self):
        while not self.controller.shutdown:
            self.controller.update_motors()
            frame = self.camera.capture()
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
            detections = self.object_model.detect(frame)

            if self.controller.collect_data:
                self.data_collector.add_data(frame, detections, self.controller.serial_output)

        self.data_collector.save_dset()
