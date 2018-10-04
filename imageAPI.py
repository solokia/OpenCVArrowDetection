import numpy as np
import cv2
import imutils
import time
#x,y,face,range
class imageAPI(object):

    def __init__(self):
        #coord = coords()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.cap = cv2.VideoCapture(0)

    def setFrame(self):
        _,self.frame = self.cap.read()
        

    def getFrame(self):
        return self.frame

    def setFrameSize(self,size):

        #frame goes by [starty:endy,startx,end]

        #0square 18000
        if size == 1:
            self.frameL = self.frame[1:2,1:2]
            self.frameM = self.frame[100:-100, 200:-100]
            self.frameR = self.frame[1:2,1:2]
            self.expectedArea = 10000

        #1square 6500,6249,6239
        if size == 2:
            self.frameL = self.frame[200:-100,:220]
            self.frameM = self.frame[200:-100,180:400]
            self.frameR = self.frame[200:-100,380:]
            self.expectedArea = 5000

        #2square 2882,2991,2848
        if size == 3:
            self.frameL = self.frame[220:-100,50:220]
            self.frameM = self.frame[220:-100,220:370]
            self.frameR = self.frame[220:-100,370:530]
            self.expectedArea = 2000

        #3square 1661,1725,1689
        if size == 4: 
            self.frameL = self.frame[250:-110,120:240]
            self.frameM = self.frame[250:-110,240:360]
            self.frameR = self.frame[250:-110,380:480]
            self.expectedArea = 1000
            #increased middle frame on the right

        #4square 1100,1060,1113
        if size == 5:
            self.frameL = self.frame[270:-120,150:250]
            self.frameM = self.frame[270:-120,250:350]
            self.frameR = self.frame[270:-120,350:450]
            self.expectedArea = 600

        self.frames = (self.frameL,self.frameM,self.frameR)

    def setThresh(self,frame):
         ###set to hsv for mask ###
        #hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        #lower = np.array([0,0,80])
        #upper = np.array([200,200,255])
        #mask = cv2.inRange(hsv, lower, upper)
        #res = cv2.bitwise_and(self.frame,self.frame, mask= mask)
        ### helps to remove certain small lightings but might affect arrow when mask###


        #resized = imutils.resize(self.frame, width=300)
        #self.ratio = self.frame.shape[0] / float(resized.shape[0])
        self.ratio = 1
        resized = frame
        #resized = res
        #resize helps reduce number of pixel for calc

        blurred_frame = cv2.GaussianBlur(resized, (9, 9), 0)
        gray = cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2GRAY)
        #blur cvt to gray
        ret, self.thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        #thresh = cv2.Canny(gray,50,100)
    
    def getThresh(self):
        return self.thresh

    def setContour(self,thresh):
         _, self.contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    def getContour(self,):
        return self.contours

    def getArrow(self,approx,c) :
        x,y,w,h = cv2.boundingRect(c)

        print("in get arrow")
        if (w/h>0.85) and (w/h<1.3) and (w>30) :
            print("in w/h",w,"/",h)
            if (len(approx)>5) and (len(approx)<9):
                
                
                if (approx[1][0][1]>= (approx[len(approx)-1][0][1]-h*0.1)) and (approx[1][0][1] <= (approx[len(approx)-1][0][1]+h*0.1)) :
                    #cv2.putText(self.frame,"up",(cX,cY),font,1,(0,0,255),1)
                    #cv2.drawContours(self.frame, c, -1, (0, 255, 0), 2)
                    #cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),2)
                    print("UP arrow")
                    return True

        #################### FOR CHECKLIST TO DETECT REST OF THE ARROWS ########################

                # elif abs(minyx-maxyx)<=w*0.2 :
                #     print("minx+(maxx-minx)",minx,"+(",maxx,"-",minx,")")
                #     middleX = (minx+maxx)/2
                #     middleY = (miny+maxy)/2
                    
                #     print("minyx <middlex: ",minyx,middleX)
                #     print("minxy-middleY",minxy,middleY)
                #     print("maxxy-middleY",maxxy,middleY)
                #     if minyx<middleX and abs(minxy-middleY)<=h*0.3:
                #         cv2.putText(self.frame,"left",(cX,cY),font,1,(0,0,255),1)
                #         cv2.drawContours(self.frame, c, -1, (0, 255, 0), 2)
                #         cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),2)
                #         return True

                #     elif minyx>middleX and abs(maxxy-middleY)<=h*0.3:
                #         cv2.putText(self.frame,"right",(cX,cY),font,1,(0,0,255),1)
                #         cv2.drawContours(self.frame, c, -1, (0, 255, 0), 2)
                #         cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),2)
                #         return True

                # elif maxyLoc < len(approx)-1 :
                #     if (approx[maxyLoc-1][0][1]>= (approx[maxyLoc+1][0][1]-h*0.1)) and (approx[maxyLoc-1][0][1] <= (approx[maxyLoc+1][0][1]+h*0.1)) : 
                #         cv2.putText(self.frame,"down",(cX,cY),font,1,(0,0,255),1)
                #         cv2.drawContours(self.frame, c, -1, (0, 255, 0), 2)
                #         cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,255,0),2)
                #         return True

                # else :
                #     cv2.putText(self.frame,"nothing here",(cX,cY),font,1,(0,0,255),1)

        print("no arrow")
        return False

    def setVal(self,approx) :
        
        (self.minx,self.minxy) = approx[0][0]
        (self.maxx,self.maxxy) = approx[0][0]
        (self.minyx,self.miny) = approx[0][0]
        (self.maxyx,self.maxy) = approx[0][0]
        (self.minxLoc,self.maxxLoc,self.minyLoc,self.maxyLoc) = (0,0,0,0)
        i=0
        print("drawing")
        for p in approx:
            (x,y)=(approx[i][0][0],approx[i][0][1])
            #x*=self.ratio
            #y*=self.ratio
            x = x.astype("int")
            y = y.astype("int")

            if self.minx > x :
                (self.minx,self.minxy) = (x,y)
                self.minxLoc = i
            if self.maxx < x :
                (self.maxx,self.maxxy) = (x,y)
                self.maxxLoc = i
            if self.miny > y :
                (self.minyx,self.miny) = (x,y)
                #print ("self.minyx: ",self.minyx)
                self.minyLoc = i
            if self.maxy < y :
                (self.maxyx,self.maxy) = (x,y)
                self.maxyLoc = i
            
            
            pt = (x,y)
            print(pt)
            #cv2.circle(frame,pt,10,(0,0,200),4)
            i+=1

    def findArrow(self):
                      
        i = 0
        found = False

        for contour in self.contours:
            area = cv2.contourArea(contour)
            c = contour
            #before resize ~ 130k after resize 7k
            if area != 0 : 
                #M = cv2.moments(contour)
                #cX = int((M["m10"] / M["m00"]) * self.ratio)
                #cY = int((M["m01"] / M["m00"]) * self.ratio)
                #cv2.putText(self.frame,str(i),(cX,cY),font,1,(0,0,255),1)
            

                i += 1
                #c = contour.astype("float")
                #c *=self.ratio
                #c = c.astype("int")
                x,y,w,h = cv2.boundingRect(c)
                
                
                
                if(w/h>0.85)and(w/h<1.3) and area>2000:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                    #set to 2% to get 7 points
                    print("Area  ",i," : ",area)
                    #self.setVal(approx)
                    print("w/h",w,"/",h)
                    found = self.getArrow(approx,c)
                    print("approx : ",len(approx))

                
            #2% epsilon will get all corners so far
            
            
            if i >12 :
                return False
            if found :
                return True

    def run(self,dist):

        #count = {"left":0,"middle":0,"right":0}
        time.sleep(1)

        self.setFrame()
        count = [0, 0, 0]
        loopCount = 0
        while loopCount < 4 :

            self.setFrame()
            self.setFrameSize(dist)
            
            i = 0
            for frame in self.frames:
                self.setThresh(frame)
                self.setContour(self.thresh)

                if self.findArrow():
                    count[i] += 1
                
                else:
                    count[i] -= 1

                i += 1

            loopCount += 1
            time.sleep(0.2)

        for x in count:
            if(x>2):
                x = True
            else:
                x = False

       
        # clear the stream in preparation for the next frame
        #rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        cv2.imshow('famel',self.frameL)
        cv2.imshow('frameM',self.frameM)
        cv2.imshow('frameR',self.frameR)
        cv2.waitKey(0)
        
        
        cv2.destroyAllWindows()    
        
        print(count)
        return count


    def closeAPI(self):                                         
        self.cap.release()



# cv2.imshow("Frame", self.frame)
# #cv2.imshow("res", res)
# cv2.imshow("thresh", thresh)



# key = cv2.waitKey(1) & 0xFF

# # if the `q` key was pressed, break from the loop
# if key == ord("q") :
#     break
#    cv2.waitKey(0)
#    break

    

               
                        

