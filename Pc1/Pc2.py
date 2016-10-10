import socket
import Tkinter as tk
import pyaudio
import wave
import  threading
import os
import time
from array import array
from os import stat
import Main

def GetArrFromWav(name):
    arr = array('B')  # create binary array to hold the wave file
    result = stat(name)  # sample file is in the same folder
    f = open(name, 'rb')  # this will play
    arr.fromfile(f, result.st_size)  # using file size as the array length
    print("Length of data: " + str(len(arr)))
    return arr

def comp2Wav(namefile1,nameFile2):
    arr1 = GetArrFromWav(namefile1)#make wav files to arrays
    arr2 = GetArrFromWav(nameFile2)
    if(len(arr1)!=len(arr2)): #if the len not eq= false
        return False
    else:
        return arr1==arr2 # if is the same vals it is the same


global x
x=1

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(1)
s.bind((HOST, PORT))
s.listen(1) # on 127.0.0.1, use on ~~63973

print('Listening...')
# if firstTime:
conn, addr = s.accept()
print('Connected by', addr)

backNameFile = "FileBack.wav"
outfile = open(backNameFile, 'wb')

#write this msg until no data
while True:
    data = conn.recv(1024)
    if not data: break
    outfile.write(data)


conn.close()
outfile.close()
print ("Completed.")




