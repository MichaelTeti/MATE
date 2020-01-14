import cv2
import csv 


class DataCollector:
    def __init__(self, img_size=256):
        self.img_size = img_size
        self.img_count = 0
        self.dset_count = 0
        self.img_dset = [np.zeros([1000, img_size, img_size, 3], dtype=np.uint8)]
        self.object_dset = [np.zeros([1000, 10, 7])]
        self.motor_dset = [np.zeros([1000, 2])]
        
        os.mkdir('Data') if 'Data' not in os.listdir() else None 
        


    def add_data(self, img, objects, motors):
        if self.img_count == 999:
            self.img_dset[self.dset_count][self.img_count, ...] = img
            if objects is not None: self.object_dset[self.dset_count][self.img_count, :objects.shape[0], :] = objects.cpu().numpy()
            self.motor_dset[self.dset_count][self.img_count, :] = [int(v) for v in motors[:-1].split(',')]

            self.img_dset.append(np.zeros([1000, img_size, img_size, 3], dtype=np.uint8))
            self.object_dset.append(np.zeros([1000, 10, 7]))
            self.motor_dset.append(np.zeros([1000, 2]))
            self.dset_count += 1
            self.img_count = 0

        else:
            self.img_dset[self.dset_count][self.img_count, ...] = img
            if objects is not None: self.object_dset[self.dset_count][self.img_count, :objects.shape[0], :] = objects.cpu().numpy()
            self.motor_dset[self.dset_count][self.img_count, :] = [int(v) for v in motors[:-1].split(',')]
        


    def save_dset(self):
        pass
                
