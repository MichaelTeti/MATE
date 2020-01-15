import os, sys
import torch
from torch.autograd import Variable
sys.path.append('/home/mteti/PyTorch-YOLOv3')

from models import *
from utils.utils import *
from utils.datasets import *


class ObjectDetector:
    def __init__(self, model_config_path, model_weights_path, img_size=256):
        assert((model_config_path is not None and os.path.isfile(model_config_path))), \
            'ObjectDetector requires that model_config_path is not None and that the path exists.'
        assert((model_weights_path is not None and os.path.isfile(model_weights_path))), \
            'ObjectDetector requires that model_weights_path is not None and that the path exists.'

        self.model_config_path = model_config_path
        self.model_weights_path = model_weights_path  
        self.img_size = img_size      

        print('[INFO] LOADING MODEL.')
        self.load_model()
        print('[INFO] MODEL LOADED.')



    def load_model(self):
        assert(torch.cuda.is_available() and torch.cuda.device_count() >= 1), \
            'Make sure cuda is available.'
        self.model = Darknet(self.model_config_path, img_size=self.img_size).cuda()
        self.model.load_state_dict(torch.load(self.model_weights_path))
        self.model.eval()


    def to_Tensor(self, image):
        image = image[..., ::-1] / 255.
        return Variable(torch.from_numpy(image).float().cuda().permute(2, 0, 1)[None, ...])


    def detect(self, image):
        tensor = self.to_Tensor(image)

        with torch.no_grad():
            outputs = self.model(tensor)
            detections = non_max_suppression(outputs, 0.8, 0.4)[0]
            
        return detections


