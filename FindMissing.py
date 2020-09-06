def play():
    #Import Modules
    import cv2
    import numpy as np
    import face_recognition
    import os
    from playsound import playsound

    path = 'Images'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for x in myList:
        curImg = cv2.imread(f'{path}/{x}')
        images.append(curImg)
        classNames.append(os.path.splitext(x)[0])
    print(classNames)

    #encoding the images
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def play():
        mp3File = "tune.mp3"
        playsound(mp3File)

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                playsound("tune.mp3")
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)



        cv2.imshow('Webcam', img)
        cv2.waitKey(1)

#GUI
from tkinter import *
from PIL import ImageTk

class Login:
    def __init__(self,root):
        self.root=root
        self.root.title("Voice 4 the missing's")
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)
        #============================#
        self.bg=ImageTk.PhotoImage(file="front.jpg")
        self.bg_image=Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        #==============================#
        Frame_login=Frame(self.root,bg="white")
        Frame_login.place(x=150,y=150,height=340,width=500)

        title=Label(Frame_login,text="Voice 4 the missing's",font=("Impact",35,"bold"),fg="#d77577",bg="white").place(x=40,y=30)
        subtitle = Label(Frame_login, text="Click below button to get started", font=("times new roman", 20, "bold"), fg="#d77577",bg="white").place(x=40, y=120)
        Login_btn=Button(Frame_login,text="Click",fg="white",bg="#d77577",font=("times new roman",35,"bold"),command=play).place(x=150,y=200)

root=Tk()
obj=Login(root)
root.mainloop()
