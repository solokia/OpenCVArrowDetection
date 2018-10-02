#from picamera.array import PiRGBArray
#from picamera import PiCamera
#import time
import numpy as np
import cv2
import imutils


font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
 
while True:
    _, frame = cap.read()

    #_,frame = cap.read()
    #1sq
    #frame = frame[100:-50, 100:-100]
    #for 2sq
    #frame = frame[200:-100, 200:-200]


    #    if area > 50:
    #       1square = 9943
    #       2square = 3828  
    #       3square = 1723
    #       4square = 948


    expectedArea = 8000



    #img[starty:endy,startx:endx]
    #cv2.imshow("crop",crop_img)

    #resized = imutils.resize(frame, width=300)
    #ratio = frame.shape[0] / float(resized.shape[0])
    ratio = 1
    resized = frame
    #resize helps reduce number of pixel for calc

    blurred_frame = cv2.GaussianBlur(resized, (15, 15), 0)
    gray = cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2GRAY)
    #blur cvt to gray
    ret, thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #threshold to black and white
    #threshold needs more tweaking

    _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    i = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        print("Area : ",area)
        #before resize ~ 130k after resize 7k
        if area != 0 :
            M = cv2.moments(contour)
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
#            cv2.putText(frame,str(i),(cX,cY),font,1,(0,0,255),1)
        
        #x=np.array(contour[0])
        #print(x)
        
        i=i+1
        c = contour.astype("float")
        c *=ratio
        c = c.astype("int")
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        #2% epsilon will get all corners so far
        print("approx : ",len(approx))
#        cv2.drawContours(frame, c, -1, (0, 255, 0), 2)
#        if area > expectedArea and area < expectedArea+200 :
#            cv2.drawContours(frame, c, -1, (0, 255, 0), 3)
#            break
    #    if len(approx) == 7 :
    #        break
    #    
    #    so far points 7fornearest 6 for square 5 for 3
    #


    #peri = cv2.arcLength(contours[0], True)
    #approx = cv2.approxPolyDP(contours[0], 0.04 * peri, True)
    #contour[number][*][getxy]
    #approx[0][xy]

    (x,y) = approx[0][0]
    print((x,y))
    print(approx[0][0])
    #a = approx.astype("float")
    #a *= ratio
    #a = c.astype("int")
    #cv2.drawContours(frame, a, -1, (0, 255, 0), 3)
    (minx,minxy) = approx[0][0]
    (maxx,maxxy) = approx[0][0]
    (minyx,miny) = approx[0][0]
    (maxyx,maxy) = approx[0][0]
    (minxLoc,maxxLoc,minyLoc,maxyLoc) = (0,0,0,0)
    middleX = 0
    i=0
    print("drawing")
    for p in approx:
        (x,y)=(approx[i][0][0],approx[i][0][1])
        #x*=ratio
        #y*=ratio
        x = x.astype("int")
        y = y.astype("int")

        if minx > x :
            (minx,minxy) = (x,y)
            minxLoc = i
        if maxx < x :
            (maxx,maxxy) = (x,y)
            maxxLoc = i
        if miny > y :
            (minyx,miny) = (x,y)
            minyLoc = i
        if maxy < y :
            (maxyx,maxy) = (x,y)
            maxyLoc = i
        
        
        pt = (x,y)
        print(pt)
#        cv2.circle(frame,pt,1,(0,0,200),2)
        i+=1

#    if(len(approx)>3) :
#        print("minyx,maxyx : ",minyx,maxyx)
#        if (approx[1][0][1]>= (approx[len(approx)-1][0][1]-15)) and (approx[1][0][1] <= (approx[len(approx)-1][0][1]+15)) :
#            cv2.putText(frame,"up",(cX,cY),font,1,(0,0,255),1)

#        elif abs(minyx-maxyx)<=25 :
#            middleX = minx+(maxx-minx)
#            middleY = miny+(maxy-miny)
            
#            print("middleX,minyx : ",middleX,minyx)
#            if minyx<middleX and abs(minxy-middleY)<=5:
#                cv2.putText(frame,"left",(cX,cY),font,1,(0,0,255),1)
#            elif minyx>middleX and abs(maxxy-middleY)<=5:
#                cv2.putText(frame,"right",(cX,cY),font,1,(0,0,255),1)
#        elif maxyLoc != len(approx)-1 :
#            if (approx[maxyLoc-1][0][1]<= (approx[maxyLoc+1][0][1]-15)) and (approx[maxyLoc-1][0][1] >= (approx[maxyLoc+1][0][1]+15)) : 
#                cv2.putText(frame,"down",(cX,cY),font,1,(0,0,255),1)
#        else :
#            cv2.putText(frame,"nothing here",(cX,cY),font,1,(0,0,255),1)
                    



    #print("approx : ")
    #print(approx) 
    #print(len(contours))
    #print(contours[1][0])
    cv2.imshow("Frame", frame)
    cv2.imshow("Thresh",thresh)
    #rawCapture.truncate(0)
 
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    #rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("t") :
        cv2.imwrite("./square.jpg",frame)
    if key == ord("q") :
        break
#    cv2.waitKey(0)
#    break

                                     
cap.release()
cv2.destroyAllWindows()

def getArrow(frame,approx,cX,cY,minx,maxx,miny,maxy,maxyLoc) :
    
    if(len(approx)>3) :
        print("minyx,maxyx : ",minyx,maxyx)
        if (approx[1][0][1]>= (approx[len(approx)-1][0][1]-15)) and (approx[1][0][1] <= (approx[len(approx)-1][0][1]+15)) :
            cv2.putText(frame,"up",(cX,cY),font,1,(0,0,255),1)

        elif abs(minyx-maxyx)<=25 :
            middleX = minx+(maxx-minx)
            middleY = miny+(maxy-miny)
            
            print("middleX,minyx : ",middleX,minyx)
            if minyx<middleX and abs(minxy-middleY)<=5:
                cv2.putText(frame,"left",(cX,cY),font,1,(0,0,255),1)
            elif minyx>middleX and abs(maxxy-middleY)<=5:
                cv2.putText(frame,"right",(cX,cY),font,1,(0,0,255),1)
        elif maxyLoc != len(approx)-1 :
            if (approx[maxyLoc-1][0][1]<= (approx[maxyLoc+1][0][1]-15)) and (approx[maxyLoc-1][0][1] >= (approx[maxyLoc+1][0][1]+15)) : 
                cv2.putText(frame,"down",(cX,cY),font,1,(0,0,255),1)
        else :
            cv2.putText(frame,"nothing here",(cX,cY),font,1,(0,0,255),1)
                    




