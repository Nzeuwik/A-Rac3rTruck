import cv2
import time


class NoImageException(Exception):
    pass


class NoCameraException(Exception):
    pass


class ResolutionException(Exception):
    pass


class Camera(object):
    def __init__(self, device_id=0, resolution=(640, 480)):
        """
        Initialize the camera.
        :param device_id: Device id (default: /dev/video0)
        :param resolution: Camera resolution (width, height).
         Must be supported by the camera.
        """
        self.camera = cv2.VideoCapture(device_id)
        if not self.camera.isOpened():
            raise NoCameraException("Can't open device {d}".format(d=device_id))

        if self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, resolution[0]):
            raise ResolutionException("Can't set width to {w}"
                                      .format(w=resolution[0]))
        if self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, resolution[1]):
            raise ResolutionException("Can't set height to {h}"
                                      .format(w=resolution[1]))
        _ = self.next_image()  # Grab a frame to initialize

    def next_image(self):
        """
        Return the next image in the camera stream, with its timestamp
        :return: An ndarray HxWx3 for the image and the timestamp in seconds
        """
        success, image = self.camera.read()
        timestamp_s = time.time()
        if not success or image is None:
            raise NoImageException()

        return image.copy(), timestamp_s
