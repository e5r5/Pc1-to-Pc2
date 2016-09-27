import Main
import Tkinter as tk
import threading
import pyaudio
import wave
from array import array
from os import stat
import socket
import time
import os
import tkMessageBox

root = tk.Tk()  # Makes the window
root.wm_title("My pro")  # Makes the title that will appear in the top left
root.config(background="#FFFFFF")
global x
import sys

global var
var = tk.DoubleVar()
x = 0
# Left Frame and its contents
leftFrame = tk.Frame(root, width=200, height=600)
leftFrame.grid(row=0, column=0, padx=10, pady=2)

# tk.Label(leftFrame, text="Instructions:").grid(row=0, column=0, padx=10, pady=2)
# Instruct = tk.Label(leftFrame, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
# Instruct.grid(row=1, column=0, padx=10, pady=2)

try:
    imageEx = tk.PhotoImage(file='image.gif')
    tk.Label(leftFrame, image=imageEx).grid(row=2, column=0, padx=10, pady=2)
except:
    print("Image not found")

# Right Frame and its contents
rightFrame = tk.Frame(root, width=400, height=600)
rightFrame.grid(row=0, column=1, padx=10, pady=5)

circleCanvas = tk.Canvas(rightFrame, width=100, height=100, bg='white')
circleCanvas.grid(row=0, column=0, padx=10, pady=2)


class App():
    def __init__(self):
        self.isrecording = False
        photoPTT = tk.PhotoImage(file="PTT.gif")
        self.button1 = tk.Button(circleCanvas, width=80, height=80, image=photoPTT, bg='white')
        self.button1.bind("<Button-1>", self.startrecording)
        self.button1.bind("<ButtonRelease-1>", self.stoprecording)
        self.button1.image = photoPTT
        self.button1.pack(padx=3, pady=3)

    def startrecording(self, event):
        global x
        x = x + 1
        self.isrecording = True
        t = threading.Thread(target=self._record)
        t.start()

    def stoprecording(self, event):
        self.isrecording = False

    def _record(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        WAVE_OUTPUT_FILENAME = "file" + str(x) + ".wav"
        colorLog.insert(0.0, WAVE_OUTPUT_FILENAME + "\n")
        audio = pyaudio.PyAudio()
        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print "recording..."
        frames = []
        while self.isrecording:
            data = stream.read(CHUNK)
            frames.append(data)
        print "finished recording"
        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()


app = App()


def AnSendFun():
    if (x > 0):
        root3 = tk.Tk()
        for i in range(1, x + 1):
            tk.Button(root3, text="send file " + str(i), padx=20, command=lambda i=i: send(i)).grid(row=i, column=0,
                                                                                                    padx=10, pady=2)

    else:
        colorLog.insert(0.0, "No recorded yet!! " + "\n")


def sendLastFun():
    send(x)


def send(n):
    arr = array('B')  # create binary array to hold the wave file

    # sample file is in the same folder
    name = "File" + str(n) + ".wav"
    result = stat(name)
    f = open(name, 'rb')  # this will send
    arr.fromfile(f, result.st_size)  # using file size as the array length
    # print("Length of data: " + str(len(arr)))

    HOST = 'localhost'
    PORT = 50007

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(arr)
    print('Finished sending...')
    s.close()
    print('done.')


def AnPlayFun():
    if (x > 0):
        root2 = tk.Tk()
        for i in range(1, x + 1):
            tk.Button(root2, text="Play file " + str(i), padx=20, command=lambda i=i: playNum(i)).grid(row=i, column=0,
                                                                                                       padx=10, pady=2)
    else:
        colorLog.insert(0.0, "No recorded yet!! " + "\n")


def playlastFun():
    if x > 0:
        playNum(x)
    else:
        colorLog.insert(0.0, "No recorded yet!! " + "\n")


def playNum(n):
    chunk = 1024
    name = "File" + str(n) + ".wav"
    f = wave.open(r"" + name, "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()), channels=f.getnchannels(), rate=f.getframerate(),
                    output=True)

    # read data
    data = f.readframes(chunk)

    # play stream
    while data != '':
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()


def GetArrFromWav(name):
    arr = array('B')  # create binary array to hold the wave file
    result = stat(name)  # sample file is in the same folder
    f = open(name, 'rb')  # this will play
    arr.fromfile(f, result.st_size)  # using file size as the array length
    print("Length of data: " + str(len(arr)))
    # print arr
    return arr


def comp2Wav(namefile1, nameFile2):
    arr1 = GetArrFromWav(namefile1)
    arr2 = GetArrFromWav(nameFile2)
    if (len(arr1) != len(arr2)):
        return False
    else:
        return arr1 == arr2


def isOK():
    name = "File" + str(x) + ".wav"
    if comp2Wav("FileBack.wav", name):
        tkMessageBox.showinfo("!!!!!","Pc2 successfully received the message! ")
    else:
        tkMessageBox.showinfo("!!!!!","Pc2 not received the message! ")


def TestSendFun():
    # removeArr = os.listdir(os.getcwd())
    # for re in removeArr:
    #     if "file" in re:
    #         os.remove(re)
    arr = array('B')  # create binary array to hold the wave file
    name = "swapFile.wav"
    result = stat(name)  # sample file is in the same folder
    f = open(name, 'rb')  # this will play
    arr.fromfile(f, result.st_size)  # using file size as the array length
    # print("Length of data: " + str(len(arr)))

    HOST = 'localhost'  # Loopback to cheak the trans. info use on -IPv4 in TCP/IP one way rode
    PORT = 50007

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(arr)
    print('Finish sending swap File...')
    s.close()
    f.closed

    # time.sleep(1)
    ###Main.StopAll()
    t3 = threading.Thread(target=StartPC2)
    t3.start()
    # time.sleep(2)


    # time.sleep(1)
    # os.exit()
    # print "not need to print it"


def StartPC2():
    os.system('python Pc2.py')


btnFrame = tk.Frame(rightFrame, width=200, height=200)
btnFrame.grid(row=1, column=0, padx=10, pady=2)

colorLog = tk.Text(rightFrame, width=30, height=10, takefocus=0)
colorLog.grid(row=2, column=0, padx=10, pady=2)

photoAnSend = tk.PhotoImage(file="sendAn.gif")
AnSend = tk.Button(btnFrame, text="Another file to send", command=AnSendFun, image=photoAnSend)
AnSend.grid(row=0, column=0, padx=10, pady=2)

photosendLast = tk.PhotoImage(file="Send_last.gif")
sendLast = tk.Button(btnFrame, text="send last", command=sendLastFun, image=photosendLast)
sendLast.grid(row=0, column=1, padx=10, pady=2)

photoplaylast = tk.PhotoImage(file="play.gif")
playlast = tk.Button(btnFrame, text="play last", command=playlastFun, image=photoplaylast)
playlast.grid(row=0, column=2, padx=10, pady=2)

photoAnplay = tk.PhotoImage(file="playAn.gif")
Anplay = tk.Button(btnFrame, text="play another", command=AnPlayFun, image=photoAnplay)
Anplay.grid(row=0, column=3, padx=10, pady=2)
phototheTest = tk.PhotoImage(file="theTest.gif")
photoTestSend = tk.PhotoImage(file="Testsend.gif")
TestSend = tk.Button(btnFrame, text="Test send", command=TestSendFun, image=phototheTest)
TestSend.grid(row=1, column=2, padx=10, pady=2)


Testrecord = tk.Button(btnFrame, text="Test record", command=lambda: isOK(), image=photoTestSend)
Testrecord.grid(row=1, column=1, padx=10, pady=2)

root.mainloop()


