import socket
import Tkinter as tk
import pyaudio
import wave
import  threading
import os
import time
from array import array
from os import stat
import sys
import Main
def GetArrFromWav(name):
    arr = array('B')  # create binary array to hold the wave file
    result = stat(name)  # sample file is in the same folder
    f = open(name, 'rb')  # this will play
    arr.fromfile(f, result.st_size)  # using file size as the array length
    #print("Length of data: " + str(len(arr)))
    #print arr
    return arr

def comp2Wav(namefile1,nameFile2):
    arr1 = GetArrFromWav(namefile1)
    arr2 = GetArrFromWav(nameFile2)
    if(len(arr1)!=len(arr2)):
        return False
    else:
        return arr1==arr2
def gui():
    root = tk.Tk()
    root.wm_title("My pro2")
    speaker = tk.PhotoImage(file="speaker.gif")
    B = tk.Button(root, text ="Hello",width=500, height=500, image=speaker)
    B.pack()
    root.mainloop()

t = threading.Thread(target=gui)
t.start()
firstTime = True
global x
x=1
while True:

    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    print('Listening...')
    #if firstTime:
    conn, addr = s.accept()
    print('Connected by', addr)
    firstTime = False
    #time.sleep(2)
    #os.remove("newfile.wav")
    name = "file"+ str(x) + ".wav"
    #name = "FileBack.wav"
    outfile = open(name, 'ab')
    while True:
        data = conn.recv(1024)
        if not data: break
        outfile.write(data)
    s.close()
    conn.close()
    outfile.close()
    print ("Completed.")
    if(comp2Wav("swapFile.wav",name)):

        os.system('python Main.py')
        time.sleep(1)
        os.remove(name)
        sys.exit()
        print "not need to print it"
    # define stream chunk
    chunk = 1024
    # open a wav format music
    f = wave.open(name, "rb")
    x=x+1
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()), channels=f.getnchannels(), rate=f.getframerate(),output=True)

    # read data
    data = f.readframes(chunk)

    # paly stream
    while data != '':
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()



print "goodbye!"

