import cv2
from python_src.berry import Berry
from time import sleep
import collections
import threading
import numpy as np
from python_src.berry_factory import berry_class_decider

class Camera:


    def __init__(self):
        self.cam = cv2.VideoCapture(2)  # 0 -> index of camera
        self.set_1080p()
        # self.set_480p()
        self.image_count = 0
        self.berry_image = None
        self.image_buffer = None
        self.thread = None
        self.stopping_thread = True
        self.lock = threading.Lock()

    def set_1080p(self):
        self.set_res(1920, 1080)

    def set_720p(self):
        self.set_res(1280, 720)

    def set_480p(self):
        self.set_res(640, 480)

    def set_res(self, width, height):
        self.cam.set(3, width)
        self.cam.set(4, height)

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
            sleep(.005)
            with self.lock:
                _, self.image_buffer = self.cam.read()

    def capture(self):
        if self.stopping_thread:
            print('Capture called on camera while not capturing!')
            return self.image_buffer
        sleep(.05)
        with self.lock:
            self.berry_image = self.image_buffer.copy()
        # np.copy(self.image_buffer)
        self.image_count += 1
        cv2.imwrite('image_{}.png'.format(self.image_count), self.berry_image)
        return self.berry_image


def find_light(img1, img2, count):
    gimg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gimg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    diff = cv2.subtract(gimg2, gimg1)
    _, diff2 = cv2.threshold(diff, 55, 255, cv2.THRESH_BINARY)
    cv2.imwrite('diff_image_{}.png'.format(count), diff2)

    params = cv2.SimpleBlobDetector_Params()
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False
    params.filterByColor = True
    params.blobColor = 255
    # params.minThreshold = 200
    # params.maxThreshold = 255
    params.filterByArea = True
    params.maxArea = 100
    params.minArea = 5
    detector = cv2.SimpleBlobDetector_create(params)

    # diff2 = cv2.bitwise_not(diff2)
    keypoints = detector.detect(diff2)
    if len(keypoints) > 1 or len(keypoints) < 1:
        print('Found {} blobs!'.format(len(keypoints)))
        pos = (0, 0)
    else:
        print('Found location')
        pos = cv2.KeyPoint.convert(keypoints)[0]
    # diff2 = cv2.bitwise_not(diff2)
    im_with_keypoints = cv2.drawKeypoints(diff2, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite('diff_image_key_{}.png'.format(count), im_with_keypoints)
    return pos


def find_berries(berries, classesOfBerriesToFind = Berry.BerryClasses.all ):
    camera = Camera()
    camera.start_capture()
    positions = {}
    i = 0
    ledColors = {}
    print ('turning lights off')
    for berry in berries.values():
        berry.set_status_led(0)
        if (berry.berry_type == 'RGB'):
            ledColors[i] = berry.read_colors()
            berry.set_color([0, 0, 0])
            i = i + 1
    sleep (0.50)
    img_off = camera.capture()
    i = 0
    print ('capturing berries of class {}'.format(classesOfBerriesToFind))
    for berry in berries.values():
        berry_class = berry_class_decider(berry.berry_type)
        if (berry_class == classesOfBerriesToFind or classesOfBerriesToFind == Berry.BerryClasses.all):
            # get that kind of berry.
            berry.set_status_led(1)
            print('Capturing berry: {}'.format(berry.name))
            img2 = camera.capture()
            berry.set_status_led(0)
            camera.image_count += 1
            pos = find_light(img_off, img2, camera.image_count)
            positions[berry.name] = pos
        else:
            # do nothing.
            print ('skipping berry: {}'.format(berry.name))
    # now turn the lights back on.
    print ('turning lights back on')
    for berry in berries.values():
        if (berry.berry_type == 'RGB'):
            berry.set_color(ledColors[i])
            i = i + 1

    camera.stop_capture()
    return img_off, positions
