from jetcam.csi_camera import CSICamera


class Camera:
    def __init__(self, fps=10, img_size=256):
        self.fps = fps
        self.img_size = img_size
        self.cam = CSICamera(width=img_size, height=img_size, capture_width=1080, capture_height=720, capture_fps=fps)

    def capture(self):
        self.frame = self.cam.read()
        return self.frame
