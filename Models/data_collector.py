import cv2
import csv
from time import time
import numpy as np
import os 
from datetime import datetime


class DataCollector:
    def __init__(self, img_size=256, data_collection_interval=0.2):
        self.img_size = img_size
        self.data_collection_interval = data_collection_interval
        self.last_collection_time = time()
        self.initial_collection_time = self.last_collection_time
        self.img_count = 0
        self.dset_count = 0
        os.mkdir('Data') if 'Data' not in os.listdir() else None 


    def add_data(self, img, objects, motors):
        if self.dset_count == 0 and self.img_count == 0:
            self.img_dset = [np.zeros([1000, self.img_size, self.img_size, 3], dtype=np.uint8)]
            self.object_dset = [np.zeros([1000, 8, 7])]
            self.motor_dset = [np.zeros([1000, 2])]

        if time() - self.last_collection_time > self.data_collection_interval:
            self.last_collection_time = time()
            if self.img_count == 999:
                self.img_dset[self.dset_count][self.img_count, ...] = img
                self.motor_dset[self.dset_count][self.img_count, :] = [int(v) for v in motors[:-3].split(',')]
                if objects is not None: 
                    self.object_dset[self.dset_count][self.img_count, :objects.shape[0] if objects.shape[0] <= 8 else 8, :] = objects.cpu().numpy()

                self.img_dset.append(np.zeros([1000, img_size, img_size, 3], dtype=np.uint8))
                self.object_dset.append(np.zeros([1000, 8, 7]))
                self.motor_dset.append(np.zeros([1000, 2]))
                self.dset_count += 1
                self.img_count = 0

            else:
                self.img_dset[self.dset_count][self.img_count, ...] = img
                self.motor_dset[self.dset_count][self.img_count, :] = [int(v) for v in motors[:-3].split(',')]
                if objects is not None: 
                    self.object_dset[self.dset_count][self.img_count, :objects.shape[0] if objects.shape[0] <= 8 else 8, :] = objects.cpu().numpy()

                self.img_count += 1


    def save_dset(self):
        if self.last_collection_time != self.initial_collection_time:
            if self.img_count < 999:
                self.img_dset[self.dset_count] = self.img_dset[self.dset_count][:self.img_count, ...]
                self.object_dset[self.dset_count] = self.object_dset[self.dset_count][:self.img_count, ...]
                self.motor_dset[self.dset_count] = self.motor_dset[self.dset_count][:self.img_count, :]

            object_file = open(os.path.join('Data', 'objects.csv'), 'a')
            object_writer = csv.writer(object_file, delimiter=',')

            motor_file = open(os.path.join('Data', 'motor.csv'), 'a')
            motor_writer = csv.writer(motor_file, delimiter=',')

            for i_dset in range(len(self.img_dset)):
                for i_sample in range(self.img_dset[i_dset].shape[0]):
                    d = datetime.now()
                    fname = '{}_{}_{}_{}_{}_{}_{}'.format(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond)
                    cv2.imwrite(os.path.join('Data', fname+'.png'), self.img_dset[i_dset][i_sample])
                    object_sample = list(self.object_dset[i_dset][i_sample].flatten())
                    object_sample.insert(0, fname)
                    object_writer.writerow(object_sample)
                    motor_sample = list(self.motor_dset[i_dset][i_sample])
                    motor_sample.insert(0, fname)
                    motor_writer.writerow(motor_sample)

            motor_file.close()
            object_file.close()
