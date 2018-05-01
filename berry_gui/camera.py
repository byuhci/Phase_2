import cv2


def camera(self):
    # initialize the camera

    # self.berry_detection_bounding_box = berry_detection()

    cam = cv2.VideoCapture(0)  # 0 -> index of camera
    s, img = cam.read()

    if s:  # frame captured without any errors
        # namedWindow("Berry Snapper")
        img = cv2.resize(img, None, fx=2, fy=1.5)
        cv2.imshow("Berry Snapper", img)
        # img = cv2.resize(img, None, 2,2, interpolation=cv2.INTER_AREA)
        cv2.waitKey(0)
        cv2.destroyWindow("Berry Snapper")
        cv2.imwrite("CRAZY.jpg", img)  # save image
        self.berry_image = img
        self.berry_detection_bounding_box = berry_detection()

        cv2.waitKey()
