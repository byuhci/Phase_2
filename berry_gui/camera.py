import cv2
from python_src.berry import Berry
from time import sleep
import collections
import threading
import numpy as np


class Camera:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)  # 0 -> index of camera
        self.image_count = 0
        self.berry_image = None
        self.image_buffer = None
        self.thread = None
        self.stopping_thread = True

    def start_capture(self):
        self.stopping_thread = False
        self.thread = threading.Thread(target=self._continuous_capture)
        self.thread.start()
        sleep(1)

    def stop_capture(self):
        self.stopping_thread = True
        self.thread.join()

    def _continuous_capture(self):
        while not self.stopping_thread:
            _, self.image_buffer = self.cam.read()

    def capture(self):
        sleep(.2)
        self.berry_image = np.copy(self.image_buffer)
        self.image_count += 1
        cv2.imwrite('image_{}.png'.format(self.image_count), self.berry_image)
        return self.berry_image


def find_light(img1, img2, count):
    gimg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gimg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    diff = cv2.subtract(gimg2, gimg1)
    _, diff2 = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    cv2.imwrite('diff_image_{}.png'.format(count), diff2)

    params = cv2.SimpleBlobDetector_Params()
    # params.minThreshold = 200
    # params.maxThreshold = 255
    # params.filterByArea = True
    # params.maxArea = 10000
    # params.minArea = 0j
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(diff2)
    im_with_keypoints = cv2.drawKeypoints(diff2, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite('diff_image_key_{}.png'.format(count), im_with_keypoints)
    return 0, 0


def find_berries(berries):
    camera = Camera()
    camera.start_capture()
    for berry in berries.values():
        berry.set_status_led(0)
    img_off = camera.capture()
    for berry in berries.values():
        berry.set_status_led(1)
        print('Capturing berry: {}'.format(berry.name))
        img2 = camera.capture()
        berry.set_status_led(0)
        camera.image_count += 1
        pos = find_light(img_off, img2, camera.image_count)
    camera.stop_capture()
