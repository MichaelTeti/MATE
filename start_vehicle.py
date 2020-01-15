from vehicle import *
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('--camera_update_freq',
    default=10,
    type=int,
    help='The frame rate of the camera. Default is 10.')
parser.add_argument('--motor_update_freq',
    default=10,
    type=int,
    help='How many times per second to update the motors. Default 10.')
parser.add_argument('--control_mode',
    type=str,
    choices=['joystick', 'autonomous'],
    default='joystick',
    help='Whether to use the joystick for control or autonomous mode. Default is joystick.')
parser.add_argument('--model_config_path',
    type=str,
    default=None,
    help='Path to the model config file if using autonomous mode.')
parser.add_argument('--model_weights_path',
    type=str,
    default=None,
    help='Path to the model weights.')
parser.add_argument('--img_size',
    type=int,
    default=256,
    help='The size the image will be resized to for the ObjectDetector model. Default is 256.')
parser.add_argument('--data_collection_interval',
    type=float,
    default=0.3,
    help='How many seconds to wait until adding a new frame to the dataset. Default is 0.3')
parser.add_argument('--show_frame',
    type=bool,
    default=False,
    help='Whether to show the incoming frames or not. Default is False.')
args = parser.parse_args()


if __name__ == '__main__':
    Vehicle(controller=args.control_mode,
            motor_fps=args.motor_update_freq,
            cam_fps=args.camera_update_freq,
            model_config_path=args.model_config_path,
            model_weights_path=args.model_weights_path,
            data_collection_interval=args.data_collection_interval,
            img_size=args.img_size,
            show_frame=args.show_frame)
