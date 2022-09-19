from collections import UserDict
import numpy as np
import face_recognition
import cv2
from datetime import datetime
import tkinter as tk
import os
import customtkinter


def save_id():
    global userId
    userId=""
    dialog = customtkinter.CTkInputDialog(master=None, text="Type in a number:", title="Test")
    userId=dialog.get_input()
    return 0

def capture_image(userId):

    inputValue=userId
    id=inputValue.upper()+".jpg"
    key = cv2. waitKey(0)
    webcam = cv2.VideoCapture(0)

    while True:
        try:
            check, frame = webcam.read()
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)


            if key == ord('s'): 
                
                cv2.imwrite(f"{path}\{id}", img=frame)
                webcam.release()
                cv2.destroyAllWindows()
                showImage = customtkinter.CTkButton(root,text="Show Image",command=lambda: show_image(f"{path}\{id}")).place(x=80,y=20)
                # showImage=tk.Button(root,text="Show Image",command=lambda: show_image(f"{path}\{id}")).pack()
                break
            elif key == ord('q'):
                webcam.release()
                cv2.destroyAllWindows()
                break
            
        except(KeyboardInterrupt):
            webcam.release()
            cv2.destroyAllWindows()
            break

def show_image(id):

    img_new = cv2.imread(id, cv2.COLOR_BGR2RGB)
    img_new = cv2.imshow("Captured Image", img_new)

def image_load():
    path="images"
    images=[]
    classNames=[]
    myList=os.listdir(path)
    # print(myList)
    for _ in myList:
        curImg=cv2.imread(f"{path}\{_}")
        images.append(curImg)
        classNames.append(os.path.splitext(_)[0])
    # print(len(images))
    return classNames,images

def findEncoding(images):
    encodingList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        print(len(encodingList))
        # print(img)
        # break
        encode=face_recognition.face_encodings(img)[0]
        encodingList.append(encode)
    return encodingList

def face_recog():
    second=True
    cap=cv2.VideoCapture(0)


    classNames,images=image_load()
    encodinfListKnow=findEncoding(images)
    # print("encoding complete")
    while (second):
        sucess,img=cap.read()
        imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        facesCurFrame=face_recognition.face_locations(imgS)
        encodingCurFrame=face_recognition.face_encodings(imgS,facesCurFrame)

        for encodeFace,faceLoc in zip(encodingCurFrame,facesCurFrame):
            matches=face_recognition.compare_faces(encodinfListKnow,encodeFace)
            faceDis=face_recognition.face_distance(encodinfListKnow,encodeFace)
            matchIndex=np.argmin(faceDis)

            if matches[matchIndex]:
                name=classNames[matchIndex].upper()
                # print(name)
                y1,x2,y2,x1=faceLoc
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
                cv2.rectangle(img,(x1,y2),(x2,y2-35),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
                markAttendence(name)

        cv2.imshow("webcam",img)
        key=cv2.waitKey(1)
        if key==27:
                second=False
                cv2.destroyAllWindows()
                cap.release()
                break
    return 0

def markAttendence(name):
    with open("attendence.csv","r+") as f:
        myDataList=f.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(",")
            nameList.append(entry[0])
        if name not in nameList:
            now=datetime.now()
            dtString=now.strftime("%H:%M:%S")
            f.writelines(f"\n{name},{dtString}")

def exit_fun():
    global exit_val
    exit_val=False
    return root.destroy

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root=customtkinter.CTk()
root.title("Face Attendence System")
root.geometry("300x230")

path="images"

saveId = customtkinter.CTkButton(root,text = "Enter ID",command=lambda: save_id()).place(x=80,y=50)
printButton = customtkinter.CTkButton(root,text = "Click For Image",command=lambda: capture_image(userId)).place(x=80,y=80)
# saveId.place(x=175,y=200)
face_recog_button=customtkinter.CTkButton(root,text = "Start Marking",command=lambda : face_recog()).place(x=80,y=110)
exit_val =True
exit_button = customtkinter.CTkButton(root,text = "Exit",command=exit_fun()).place(x=80,y=140)

root.mainloop()
print("!!!!!!exiting!!!!!!")