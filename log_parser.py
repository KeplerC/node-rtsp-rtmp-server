import mysql.connector

mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="root",
      database="demo"
    )

# find last SR
last_sr = -1
first_pts_index = -1
first_pts = -1
ts_sender = -1
last_successful = -1

from datetime import datetime
while True:
    with open("log.txt", "r") as f:
        a = f.read()
        l = a.split("\n")
    give_up = False
    for i in range(len(l)-1, 0, -1):
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
