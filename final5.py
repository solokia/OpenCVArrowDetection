import numpy as np
import cv2
import imutils
import math

font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
 
while True:

#frame = cv2.imread("square2.jpg")
#LTMTRT
#

    _,frame = cap.read()
    frame = frame[100:-100,:]



    areabuffer = 0
    (x,y) = (0,0)
    (minx,minxy) = (0,0)
    (maxx,maxxy) = (0,0)
    (minyx,miny) = (0,0)
    (maxyx,maxy) = (0,0)
    (minxLoc,maxxLoc,minyLoc,maxyLoc) = (0,0,0,0)


    def setVal(approx) :
        global x,y,minx,minxy,maxx,maxxy,minyx,miny,maxyx,maxy,minxLoc,maxxLoc,minyLoc,maxyLoc
        (minx,minxy) = approx[0][0]
        (maxx,maxxy) = approx[0][0]
        (minyx,miny) = approx[0][0]
        (maxyx,maxy) = approx[0][0]
        (minxLoc,maxxLoc,minyLoc,maxyLoc) = (0,0,0,0)
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
                #print ("minyx: ",minyx)
                minyLoc = i
            if maxy < y :
                (maxyx,maxy) = (x,y)
                maxyLoc = i
            
            
            pt = (x,y)
            print(pt)
            #cv2.circle(frame,pt,10,(0,0,200),4)
            i+=1


    def getArrow(frame,approx,c,cX,cY,minx,maxx,miny,maxy,minyx,maxyx,maxyLoc) :
        x,y,w,h = cv2.boundingRect(c)

        print("in get arrow")
        if(w/h>0.85) and (w/h<1.3) and (w>30) :
            print("in w/h",w,"/",h)
            if(len(approx)>5) and (len(approx)<9) :
                print("minyx,maxpyx : ",minyx,maxyx)
                
                
                if (approx[1][0][1]>= (approx[len(approx)-1][0][1]-h*0.1)) and (approx[1][0][1] <= (approx[len(approx)-1][0][1]+h*0.1)) :
                    cv2.putText(frame,"up",(cX,cY),font,1,(0,0,255),1)
                    cv2.drawContours(frame, c, -1, (0, 255, 0), 2)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    print("Inverse Tang left : ",(math.atan((approx[1][0][1]-approx[0][0][1])/(approx[1][0][0]-approx[0][0][0]))))
                    print("Inverse Tang right : ",(math.atan((approx[len(approx)-1][0][1]-approx[0][0][1])/(approx[len(approx)-1][0][0]-approx[0][0][0]))))
                    
                    return True

                elif abs(minyx-maxyx)<=w*0.2 :
                    print("minx+(maxx-minx)",minx,"+(",maxx,"-",minx,")")
                    middleX = (minx+maxx)/2
                    middleY = (miny+maxy)/2
                    
                    print("minyx <middlex: ",minyx,middleX)
                    print("minxy-middleY",minxy,middleY)
                    print("maxxy-middleY",maxxy,middleY)
                    if minyx<middleX and abs(minxy-middleY)<=h*0.3:
                        cv2.putText(frame,"left",(cX,cY),font,1,(0,0,255),1)
                        cv2.drawContours(frame, c, -1, (0, 255, 0), 2)
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        return True

                    elif minyx>middleX and abs(maxxy-middleY)<=h*0.3:
                        cv2.putText(frame,"right",(cX,cY),font,1,(0,0,255),1)
                        cv2.drawContours(frame, c, -1, (0, 255, 0), 2)
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        return True

                elif maxyLoc < len(approx)-1 :
                    if (approx[maxyLoc-1][0][1]>= (approx[maxyLoc+1][0][1]-h*0.1)) and (approx[maxyLoc-1][0][1] <= (approx[maxyLoc+1][0][1]+h*0.1)) : 
                        cv2.putText(frame,"down",(cX,cY),font,1,(0,0,255),1)
                        cv2.drawContours(frame, c, -1, (0, 255, 0), 2)
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                        return True

                else :
                    cv2.putText(frame,"nothing here",(cX,cY),font,1,(0,0,255),1)
        return False


    #1sq frame[y,x]
    #frame = frame[100:-50, 100:-100]
    #for 2sq
    #frame = frame[200:-100, 200:-200]

    # video frame is 640 * 480

    #0square 18000
    #frame = frame[100:-100, 200:-100]

    #1square 6500,6249,6239
    #frameL = frame[200:-100,:200]
    #frameM = frame[200:-100,200:400]
    #frameR = frame[200:-100,420:]

    #cv2.imshow("FrameL", frameL)
    #cv2.imshow("FrameM", frameM)
    #cv2.imshow("FrameR", frameR)

    #2square 2882,2991,2848
    #frame = frame[220:-100,50:220]
    #frameM = frame[220:-100,220:370]
    #frameR = frame[220:-100,370:530]

    #cv2.imshow("FrameL", frameL)
    #cv2.imshow("FrameM", frameM)
    #cv2.imshow("FrameR", frameR)

    #3square 1661,1725,1689 
    #frameL = frame[250:-110,120:240]
    #frameM = frame[250:-110,240:360]
    #frameR = frame[250:-110,360:480]

    #cv2.imshow("FrameL", frameL)
    #cv2.imshow("FrameM", frameM)
    #cv2.imshow("FrameR", frameR)

    #4square 1100,1060,1113
    #frameL = frame[270:-120,150:250]
    #frameM = frame[270:-120,250:350]
    #frameR = frame[270:-120,350:450]

    #cv2.imshow("FrameL", frameL)
    #cv2.imshow("FrameM", frameM)
    #cv2.imshow("FrameR", frameR)


    #    if area > 50:
    #       1square = 9943
    #       2square = 3828  
    #       3square = 1723
    #       4square = 948
    #       5square = 400


    expectedArea = 2800

    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #lower = np.array([0,0,80])
    #upper = np.array([200,200,255])
    
    #mask = cv2.inRange(hsv, lower, upper)
    #res = cv2.bitwise_and(frame,frame, mask= mask)


    #img[starty:endy,startx:endx]
    #cv2.imshow("crop",crop_img)

    #resized = imutils.resize(frame, width=300)
    #ratio = frame.shape[0] / float(resized.shape[0])
    ratio = 1
    resized = frame
    #resized = res
    #resize helps reduce number of pixel for calc

    blurred_frame = cv2.GaussianBlur(resized, (9, 9), 0)
    gray = cv2.cvtColor(blurred_frame,cv2.COLOR_BGR2GRAY)
    #blur cvt to gray
    ret, thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #thresh = cv2.Canny(gray,50,100)

    #threshold to black and white
    #threshold needs more tweaking

    _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    i = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        
        #before resize ~ 130k after resize 7k
        if area != 0 : 
            M = cv2.moments(contour)
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            #cv2.putText(frame,str(i),(cX,cY),font,1,(0,0,255),1)
        
        #x=np.array(contour[0])
        #print(x)
        
        
        i=i+1
        c = contour.astype("float")
        c *=ratio
        c = c.astype("int")
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        x,y,w,h = cv2.boundingRect(c)
        if(w/h>0.85)and(w/h<1.3) and area>200:
            print("Area  ",i," : ",area)
            setVal(approx)
            print("w/h",w,"/",h)
            getArrow(frame,approx,c,cX,cY,minx,maxx,miny,maxy,minyx,maxyx,maxyLoc)
            
        #2% epsilon will get all corners so far
        print("w/h : ",w/h)
        print("approx : ",len(approx))
        if i >12 :
            break
        
        # if area > expectedArea and area < expectedArea+1000 :
        # #if len(approx) == 10:
        #     cv2.drawContours(frame, c, -1, (0, 255, 0), 3)
        #     break
    #    if len(approx) == 7 :
    #        break
    #    
    #    so far points 7fornearest 6 for square 5 for 3
    #


    #peri = cv2.arcLength(contours[0], True)
    #approx = cv2.approxPolyDP(contours[0], 0.04 * peri, True)
    #contour[number][*][getxy]
    #approx[0][xy]

    # (x,y) = approx[0][0]

    # #a = approx.astype("float")
    # #a *= ratio
    # #a = c.astype("int")
    # #cv2.drawContours(frame, a, -1, (0, 255, 0), 3)
    # (minx,minxy) = approx[0][0]
    # (maxx,maxxy) = approx[0][0]
    # (minyx,miny) = approx[0][0]
    # (maxyx,maxy) = approx[0][0]
    # (minxLoc,maxxLoc,minyLoc,maxyLoc) = (0,0,0,0)
    # middleX = 0
    # i=0
    # print("drawing")
    # for p in approx:
    #     (x,y)=(approx[i][0][0],approx[i][0][1])
    #     #x*=ratio
    #     #y*=ratio
    #     x = x.astype("int")
    #     y = y.astype("int")

    #     if minx > x :
    #         (minx,minxy) = (x,y)
    #         minxLoc = i
    #     if maxx < x :
    #         (maxx,maxxy) = (x,y)
    #         maxxLoc = i
    #     if miny > y :
    #         (minyx,miny) = (x,y)
    #         minyLoc = i
    #     if maxy < y :
    #         (maxyx,maxy) = (x,y)
    #         maxyLoc = i
        
        
    #     pt = (x,y)
    #     print(pt)
    #     #cv2.circle(frame,pt,10,(0,0,200),4)
    #     i+=1

    # print("minyx,maxyx : ",minyx,maxyx)
    # if(len(approx)>3) :
    #     print("minyx,maxyx : ",minyx,maxyx)
    #     if (approx[1][0][1]>= (approx[len(approx)-1][0][1]-5)) and (approx[1][0][1] <= (approx[len(approx)-1][0][1]+5)) :
    #         cv2.putText(frame,"up",(cX,cY),font,1,(0,0,255),1)

    #     elif abs(minyx-maxyx)<=25 :
    #         middleX = minx+(maxx-minx)
    #         middleY = miny+(maxy-miny)
            
    #         print("middleX,minyx : ",middleX,minyx)
    #         if minyx<middleX and abs(minxy-middleY)<=5:
    #             cv2.putText(frame,"left",(cX,cY),font,1,(0,0,255),1)
    #         elif minyx>middleX and abs(maxxy-middleY)<=5:
    #             cv2.putText(frame,"right",(cX,cY),font,1,(0,0,255),1)
    #     elif maxyLoc != len(approx)-1 :
    #         if (approx[maxyLoc-1][0][1]<= (approx[maxyLoc+1][0][1]-5)) and (approx[maxyLoc-1][0][1] >= (approx[maxyLoc+1][0][1]+5)) : 
    #             cv2.putText(frame,"down",(cX,cY),font,1,(0,0,255),1)
    #     else :
    #         cv2.putText(frame,"nothing here",(cX,cY),font,1,(0,0,255),1)
                    



    #print("approx : ")
    #print(approx) 
    #print(len(contours))
    #print(contours[1][0])
    cv2.imshow("Frame", frame)
    #cv2.imshow("res", res)
    cv2.imshow("thresh", thresh)



    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    #rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q") :
        break
#    cv2.waitKey(0)
#    break

                                     
cap.release()


cv2.waitKey(0)


cv2.destroyAllWindows()

           
                    

