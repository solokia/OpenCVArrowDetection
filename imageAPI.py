from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import cv2
import imutils
import time
import json
import os


# x,y,face,range
class imageAPI(object):

    # initialization
    def __init__(self):
        # Font to show the arrow
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        # Video Stream initialization and grab reference to raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 30
        self.raw_capture = PiRGBArray(self.camera, size=(640, 480))

        # warmup the camera
        time.sleep(0.1)

        self.start = time.time()
        self.dirname = "images" + str(self.start)
        self.tmp_folder = "tmp" + str(self.start)
        os.mkdir(self.dirname)
        os.mkdir(self.tmp_folder)

    def captureImage(self, key):
        for frame in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            image = frame.array
            print('[IMAGE] captured one image with key %s' % (key))
            cv2.imwrite(self.tmp_folder + '/{}.jpg'.format(key), image)
            self.raw_capture.truncate(0)
            break

    # To set the frame size according to the distance
    def setFrameSize(self, frame, size):

        # frame goes by [starty:endy,startx,end]
        # frameL = frame[1:2, 1:2]
        frameM = frame[:-50, :400]
        frameR = frame[:-50, 300:]
        # expectedArea = 10000

        # frameL is not used now
        frames = (frameM, frameR)
        return frames

    def setThresh(self, frame):
        resized = frame

        blurred_frame = cv2.GaussianBlur(resized, (15, 15), 0)
        gray = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    # Setting the contour according to the thresh hold value
    def setContour(self, thresh):
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        return contours

    # To determine if the arrow is present in the image
    def getArrow(self, approx, c):
        x, y, w, h = cv2.boundingRect(c)

        # print("in get arrow")
        if (w / h > 0.85) and (w / h < 1.3) and (w > 30):
            # print("in w/h", w, "/", h)
            if (len(approx) > 5) and (len(approx) < 9):
                if (approx[1][0][1] >= (approx[len(approx) - 1][0][1] - h * 0.1)) and (approx[1][0][1] <= (approx[len(approx) - 1][0][1] + h * 0.1)):
                    # print("UP arrow")
                    return True
        # print("no arrow")
        return False

    # To find the arrow in the image
    def findArrow(self, contours):
        found_area_cnt = 0
        found = False
        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            # print('area', area)
            if area != 0:
                found_area_cnt += 1
                x, y, w, h = cv2.boundingRect(contour)
                if (w / h > 0.85) and (w / h < 1.3) and area > 10000:
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                    # set to 2% to get 7 points
                    found = self.getArrow(approx, contour)
                    # print("Area  ", found_area_cnt, " : ", area)
                    # print("w/h", w, "/", h)
                    # print("approx : ", len(approx))

            # 2% epsilon will get all corners so far
            if found_area_cnt > 30:
                return False
            if found:
                return True

    def run(self):
        """
        check tmp folder whether there is image inside.
        if there, is process one image, and return the (key, answer)
        key is the key algo sent
        answer is the image detection result whether there is image or not

        :return: has_pending_file, key, answer
        """
        has_pending_file = False
        files_to_be_processed = os.listdir(self.tmp_folder)
        if len(files_to_be_processed) == 0:
            return False, None, None

        print('[IMAGE] pending files count: %s' % (len(files_to_be_processed)))
        for file_name in files_to_be_processed:
            if file_name[-4:] != '.jpg':
                continue
            print('[IMAGE] processing %s' % (self.tmp_folder + '/' + file_name))
            has_pending_file = True
            key = file_name[:-4]
            try_to_read = True
            while try_to_read:
                try:
                    frame = cv2.imread(self.tmp_folder + '/' + file_name)
                    if frame is not None:
                        try_to_read = False
                except:
                    try_to_read = True

            answers = []
            frames = self.setFrameSize(frame, 1)  # currently, size is always 1
            for idx, cropped_frame in enumerate(frames):
                threshold = self.setThresh(cropped_frame)
                contours = self.setContour(threshold)
                if self.findArrow(contours):
                    print('[IMAGE] detected one arrow in frame %s with key %s' % (idx, key))
                    answers.append(True)
                    truename = "./images" + str(self.start) + "/true" + str(key) + ".jpg"
                    cv2.imwrite(truename, frame)
                else:
                    answers.append(False)

                # savename = "./images" + str(self.start) + "/M" + key + '.jpg'
                # cv2.imwrite(savename, cropped_frame)

            # imagename = "./images" + str(self.start) + "/" + str(key) + ".jpg"
            # cv2.imwrite(imagename, frame)
            os.remove(self.tmp_folder + '/' + file_name)
            print('[IMAGE] processed %s %s' % (self.tmp_folder + '/' + file_name, answers))
            return has_pending_file, key, ';'.join(['1' if answer is True else '0' for answer in answers])
        return False, None, None

    # Release of resources (camera)
    def closeAPI(self):
        print ("Closing Camera")
        self.camera.close()
        cv2.destroyAllWindows()
