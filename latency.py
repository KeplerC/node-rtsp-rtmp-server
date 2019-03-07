import mysql.connector
import numpy as np
import face_recognition
import threading
import cv2
from PIL import Image
from imutils.video import WebcamVideoStream

def proc(addr):
    video_capture = WebcamVideoStream(src="rtsp://localhost:80/" + addr).start()   
    #video_capture = cv2.VideoCapture("rtsp://localhost:80/" + addr)
    process_this_frame = True
    while True:
        try:
            frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        except:
            print("No Frame Read")
            return
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if(face_locations):
                print(face_locations)
                for i in range(len(face_locations)):
                    top, right, bottom, left = face_locations[i]
                    face_image = rgb_small_frame[top:bottom, left:right]
                    pil_image = Image.fromarray(face_image)
                    pil_image.save("/var/www/html/demo/images/face" + str(i + 1) + ".png")
                    print("saved")
            else:
                print("No Face Detected")
        process_this_frame = not process_this_frame


    
mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="root",
      database="demo"
    )

first_pts = -1
ts_sender = -1
last_lat = 1
frame_counter=1
latency = -1
import sys
from datetime import datetime
while True:
    line = sys.stdin.readline()
    if not line:
        continue
    print(line)

    if "uploading" in line:
        addr = line.split("stream ")[1]
        t = threading.Thread(target=proc, args=(addr,))
        t.start()
    if "ntp_raw" in line and int(line.split(": ")[1].split(",")[0]) > 10000000:
         ts_s = int(line.split(": ")[1].split(",")[0])
         ts_ms = int(line.split(": ")[1].split(",")[1][:4])
         ts_sender = ts_s + ts_ms * 0.0001
         #print(ts_s, ts_ms, ts_sender)
         first_pts = -1

    if "pts" in line:
        ntp_s = datetime.strptime(line.split(" p")[0], "%Y-%m-%d  %H:%M:%S.%f").timestamp()
        cur_pts = int(line.split(": ")[-1])
        latency = - ts_sender  +  ntp_s  - (cur_pts - first_pts) / 90000
        if first_pts == -1:
            first_pts = cur_pts
        #print(ts_sender, ntp_s, cur_pts, first_pts)
        #print(latency)

    #latency = latency +  0.583
    print(latency)
    if first_pts != -1 and latency > 0:
        #NOTE: uncomment for true value, this is just code for the average
        #'''
        latency = (latency + frame_counter * last_lat) / (frame_counter + 1)
        frame_counter += 1
        last_lat = latency
        print(latency)
        #'''
        mycursor = mydb.cursor()
        sql = "INSERT INTO mobiqdemo (timestamp, latency) VALUES (%s, %s)"
        val = (str(datetime.now().timestamp()), str(latency))
        mycursor.execute(sql, val)
        mydb.commit()
                                
         

'''
from datetime import datetime
while True:
    with open("log.txt", "r") as f:
        a = f.read()
        l = a.split("\n")
    give_up = False
    for i in        latency = - ts_sender  +  ntp_s  - (cur_pts - first_pts) / 90000
 range(len(l)-1, 0, -1):
        if "ntp_raw" in l[i] and int(l[i].split(": ")[1].split(",")[0]) > 10000000 :
            last_sr = i
            if last_sr <= last_successful:
                give_up = True
                break
        
            ts_s = int(l[i].split(": ")[1].split(",")[0])
            ts_ms = int(l[i].split(": ")[1].split(",")[1][:4])
            ts_sender = ts_s + ts_ms * 0.0001
            print(ts_s, ts_ms, ts_sender)
            found = False
            for j in range(i, len(l)):
                if "pts" in l[j]:
                    first_pts_index = j
                    first_pts = int(l[j].split(": ")[-1])
                    found = True
                    break
            if found:
                break
    if give_up:
        continue
        pass
    else:
        print(l[last_sr])
    import numpy as np 
    arr = []
    for i in range(first_pts_index, len(l)):
        if not "pts" in l[i]:
            continue
        ntp_s = datetime.strptime(l[i].split(" p")[0], "%Y-%m-%d  %H:%M:%S.%f").timestamp()
        cur_pts = int(l[i].split(": ")[-1])
        
        latency = - ts_sender  +  ntp_s  - (cur_pts - first_pts) / 90000
        print(ts_sender, ntp_s, cur_pts, first_pts)
        arr.append(latency * 1000)

    mycursor = mydb.cursor()

    sql = "INSERT INTO mobiqdemo (timestamp, latency) VALUES (%s, %s)"
    #val = (str(datetime.now().timestamp()), str(np.mean(arr)))
    val = (str(datetime.now().timestamp()), str(latency))
    print(np.mean(arr),latency)
    mycursor.execute(sql, val)

    mydb.commit()
    last_successful = last_sr
'''
