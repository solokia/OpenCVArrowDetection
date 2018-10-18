from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import cv2
import imutils
import time
import json

# x,y,face,range
class imageAPI(object):

    # initialization
    def __init__(self):
        global camera,rawCapture
        # coord = coords()
        # Font to show the arrow
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        # Video Stream initialization and grab reference to raw camera capture
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.framerate = 30
        rawCapture = PiRGBArray (camera,size=(640,480))
        #warmup the camera
        time.sleep(0.1)
        #self.cap = cv2.VideoCapture(0)

    def videoStart(self):
        global camera, rawCapture, image

        #capture frames from camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            #grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
            image = frame.array

            cv2.imwrite('imageTest.png', image)
            rawCapture.truncate(0)
            break

    def setFrame(self):
        global frame
        # _, self.frame = self.cap.read()
        self.frame = cv2.imread('imageTest.png')

    def getFrame(self):
        return self.frame

    # To set the frame size according to the distance
    def setFrameSize(self, size):

        # frame goes by [starty:endy,startx,end]
        self.frameL = self.frame[1:2, 1:2]
        self.frameM = self.frame[:-50, :400]
        self.frameR = self.frame[:-50, 300:]
        self.expectedArea = 10000

        # 0square 18000
        if size == 1:
            self.frameL = self.frame[1:2, 1:2]
            self.frameM = self.frame[:-50, :400]
            self.frameR = self.frame[:-50, 300:]
            self.expectedArea = 10000

        # 1square 6500,6249,6239
        if size == 2:
            self.frameL = self.frame[200:-100, :220]
            self.frameM = self.frame[200:-100, 180:400]
            self.frameR = self.frame[200:-100, 380:]
            self.expectedArea = 5000

        # 2square 2882,2991,2848
        if size == 3:
            self.frameL = self.frame[220:-100, 50:220]
            self.frameM = self.frame[220:-100, 220:370]
            self.frameR = self.frame[220:-100, 370:530]
            self.expectedArea = 2000

        # 3square 1661,1725,1689
        if size == 4:
            self.frameL = self.frame[250:-110, 120:240]
            self.frameM = self.frame[250:-110, 240:360]
            self.frameR = self.frame[250:-110, 380:480]
            self.expectedArea = 1000
            # increased middle frame on the right

        # 4square 1100,1060,1113
        if size == 5:
            self.frameL = self.frame[270:-120, 150:250]
            self.frameM = self.frame[270:-120, 250:350]
            self.frameR = self.frame[270:-120, 350:450]
            self.expectedArea = 600

        self.frames = (self.frameL, self.frameM, self.frameR)
        
        savename="./images/M"+self.testname
        cv2.imwrite(savename,self.frameM)
        savename="./images/R"+self.testname
        cv2.imwrite(savename,self.frameR)
        

    # To set the threshhold value for contours
    def setThresh(self, frame):

        ###set to hsv for mask ###
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        lower = np.array([0,0,180])
        upper = np.array([80,80,255])
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((9,9),np.uint8)
        dilation = cv2.dilate(mask,kernel,iterations = 1)
        mask = dilation
        res = cv2.bitwise_and(self.frame,self.frame, mask= mask)
        ### helps to remove certain small lightings but might affect arrow when mask###


        #resized = imutils.resize(self.frame, width=300)
        #self.ratio = self.frame.shape[0] / float(resized.shape[0])
        self.ratio = 1
        #resized = frame
        resized = res
        #resize helps reduce number of pixel for calc

        blurred_frame = cv2.GaussianBlur(resized, (15, 15), 0)
        gray = cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2GRAY)
        #blur cvt to gray
        ret, self.thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # thresh = cv2.Canny(gray,50,100)

    # Setting the contour according to the thresh hold value
    def setContour(self, thresh):
        _, self.contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # To determine if the arrow is present in the image
    def getArrow(self, approx, c):
        x, y, w, h = cv2.boundingRect(c)

        print("in get arrow")
        if (w / h > 0.85) and (w / h < 1.3) and (w > 30):
            print("in w/h", w, "/", h)
            if (len(approx) > 5) and (len(approx) < 9):

                if (approx[1][0][1] >= (approx[len(approx) - 1][0][1] - h * 0.1)) and (
                        approx[1][0][1] <= (approx[len(approx) - 1][0][1] + h * 0.1)):
                    print("UP arrow")
                    return True

        print("no arrow")
        return False

    # To find the arrow in the image
    def findArrow(self):

        i = 0
        found = False
	print('len', len(self.contours))
        for contour in self.contours:
            area = cv2.contourArea(contour)
            c = contour
            print('area', area)
            # before resize ~ 130k after resize 7k
            if area != 0:

                i += 1
                # Declare boundaries for arrow detection
                x, y, w, h = cv2.boundingRect(c)
                
                print(x, y, w, h)
                if (w / h > 0.85) and (w / h < 1.3) and area > 2000:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                    # set to 2% to get 7 points
                    print("Area  ", i, " : ", area)
                    print("w/h", w, "/", h)
                    found = self.getArrow(approx, c)
                    print("approx : ", len(approx))

            # 2% epsilon will get all corners so far
            print('i', i)
            if i > 30:
                return False
            if found:
                return True

    # Run to determine if arrow is present in the image taken by the camera
    def run(self, dist):

        # count = {"left":0,"middle":0,"right":0}
        datastore = json.loads(dist)
        rpos=datastore["robotPosition"]
        self.testname = str(rpos)+".jpg"
        arrow = datastore["arrow"]
        # time.sleep(1)
        self.start = time.time()



        #self.setFrame()
        count = [0, 0, 0]
        loopCount = 0
        while loopCount < 1:
            print("Image setting frame")
            self.setFrame()
            #cv2.imshow('start', self.frame)
            self.setFrameSize(arrow[0])
            i = 0
            for frame in self.frames:
                self.setThresh(frame)
                self.setContour(self.thresh)
                print("checking frame ",i)
                if self.findArrow():
                    count[i] += 1

                i += 1

            loopCount += 1
            print("loopCount : ", loopCount)
            print("Time taken so far : ", (time.time() - self.start))
            # time.sleep(0.2)

        #save picture name as position of robot followed by unix time
        #imagename = "./"+str(rpos)+"T"+str(time.time())+".jpg"
        imagename = "./images/"+str(rpos)+".jpg"
        cv2.imwrite(imagename, self.frame)
        truename = "./images/true"+str(rpos)+".jpg"
        i=1
        for x in count:
            if (x > 0):
                arrow[i] = True
                cv2.imwrite(truename, self.frame)
            else:
                arrow[i] = False
            i += 1
        # clear the stream in preparation for the next frame
        # rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        # self.cap.release()
        
        datastore["arrow"] = arrow
        print("IMAGE IS WRITING RETURN VALUE BELOW:")
        print(json.dumps(datastore))

        return json.dumps(datastore)

    # Release of resources (camera)
    def closeAPI(self):
        #self.cap.release()
        print ("Closing Camera")
        global camera
        camera.close()
        cv2.destroyAllWindows()






