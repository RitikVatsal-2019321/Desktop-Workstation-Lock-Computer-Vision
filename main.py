import cv2
import time
import datetime
import warnings
import numpy

vid=cv2.VideoCapture(0)

frame=vid.read()

# time.sleep(3)
def AntiSpy(alert_cnt):
    frm_1=None;
    # time.sleep(3)
    timer=0
    alert=0

    while True:
        _,frm=vid.read()
        frm=cv2.flip(frm, 1)
        timer = timer + 1
        proc=cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        proc=cv2.GaussianBlur(proc,(21,21),0)

        if frm_1 is None:
            frm_1=proc
            continue

        diff=cv2.absdiff(frm_1,proc)
        err=cv2.threshold(diff, 30,255,cv2.THRESH_BINARY)[1]
        err=cv2.dilate(err,None, iterations=0)
        (cnts,_)=cv2.findContours(err.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for contour in cnts:
            if cv2.contourArea(contour)<1000:
                continue
            (x,y,w,h)=cv2.boundingRect(contour)
            cv2.rectangle(frm,(x,y),(x+w,y+h),(0,255,0),3)
            alert=alert+1


        # cv2.imshow("Gray", proc)
        cv2.imshow("| COMPUTER VISION |", err)
        cv2.imshow('| LIVE FEED |', frm)

        if alert>=3000 and timer>=300:
            alert_cnt=alert_cnt+1
            cv2.putText(frm, '{}'.format(datetime.datetime.now()), (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 240, 255), 3)
            cv2.imwrite("Alerts\{}.jpg".format(alert_cnt), frm)
            alert=0
            timer=0


        key=cv2.waitKey(1)
        # print(key)
        if key!=-1:
            break
    return alert_cnt

if __name__=="__main__":
    strt = numpy.zeros((200, 900, 3))
    start = "--- Welcome to Workstation Lock ---"
    start2 = "Arming in 5 Seconds. Press any key to start now."
    cv2.putText(strt, start, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (69, 255, 56), 2)
    cv2.putText(strt, start2, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (96, 255, 56), 2)

    cv2.imshow("| WELCOME |", strt)
    cv2.waitKey(5000)

    cv2.destroyAllWindows()

    alert_cnt = 0
    alert_cnt=AntiSpy(alert_cnt)
    cv2.destroyAllWindows()

    img = numpy.zeros((200, 900, 3))
    clsng="You have " + str(alert_cnt) + " Alerts!!"
    clsng2="Check Folder for Images. Press any key to exit..."
    cv2.putText(img, clsng, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(img, clsng2, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("| ALERTS |", img)
    cv2.waitKey(0)
    vid.release()
    cv2.destroyAllWindows()
