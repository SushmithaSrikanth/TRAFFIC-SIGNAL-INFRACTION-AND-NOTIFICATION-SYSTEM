#for extracting foreground mask
import cv2
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import date
from datetime import datetime

now = datetime.now()
today = date.today()
vidcap=cv2.VideoCapture("test.mp4")  #getting video
car=0
ret,frame1=vidcap.read()  #reading the first frame
while vidcap.isOpened():
    ret,frame2=vidcap.read()  #reading the second frame
    frame=frame2.copy()
    if not ret:
        break
    fgmask=cv2.absdiff(frame1,frame2)
    _,thresh = cv2.threshold(fgmask,50,225,cv2.THRESH_BINARY)
    cv2.line(frame,(300,230),(800,230),(0,0,255),2) #red line
    cv2.line(frame,(300,220),(800,220),(0, 255, 0), 1) #above offset
    cv2.line(frame,(300,240),(800,240),(0, 255, 0), 1) #below offset
    thresh=cv2.cvtColor(thresh,cv2.COLOR_BGR2GRAY)
    conts,hec=cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for c in conts:
        if cv2.contourArea(c)<900:
            continue
        x,y,w,h=cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        xmid=int((x + (x +w )) / 2)
        ymid=int((y + (y + h)) / 2)
        cv2.circle(frame,(xmid,ymid),5,(0,0,0),5)

        if ymid>230 and ymid<240:
            Date = today.strftime("%B %d, %Y")
            Time = now.strftime("%H:%M:%S")
            Event = "Rule violation - Red Light skipped"
            Latitude_Longitude = "11.0952° N, 77.1514° E"
            Location = "kaniyur toll plaza, near Neelambur, Coimbatore, Tamil Nadu"
            env_path = Path('.') / '.env'
            load_dotenv(dotenv_path=env_path)
            alert_content = (f'\n\t{Event} has occured \n\t********************* \n Date : {Date} \n Time: {Time} \n Location : {Location} \n Latitude & Longitude : {Latitude_Longitude} .')
            client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
            client.chat_postMessage(channel='#neelambur_police', text=alert_content)
            car+=1
    cv2.imshow("foreground mask",thresh) #getting the foreground of frames
    cv2.putText(frame,"cars:{}".format(car),(250,50),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3)
    cv2.imshow("video", frame)

    frame1=frame2

    if cv2.waitKey(1) & 0xFF==ord('q'):#wait for key to pressed for exititng
        break;
cv2.destroyAllWindows()
vidcap.release()

