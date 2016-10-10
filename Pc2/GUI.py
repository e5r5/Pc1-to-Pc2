
import Tkinter as tk
import threading
import pyaudio
import wave
from array import array
from os import stat
import socket
import time
import os

global x


x=0



def sendLastFun():
    send(x)

def send(n):
    time.sleep(2)
    arr = array('B')  # create binary array to hold the wave file
    name = "File" + str(n) + ".wav"
    result = stat(name)
    f = open(name, 'rb')  # this will send
    arr.fromfile(f, result.st_size)  # using file size as the array length
    #print("Length of data: " + str(len(arr)))

    HOST = 'localhost'#Loopback to cheak the trans. info use on -IPv4 in TCP/IP one way rode
    PORT = 50007

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(arr)
    print('Finished sending...')
    s.close()
    f.closed
    print('done.')


def TestSendFun():
    arr = array('B')  # create binary array to hold the wave file
    name = "swapFile.wav"
    result = stat(name)  # sample file is in the same folder
    f = open(name, 'rb')  # this will play
    arr.fromfile(f, result.st_size)  # using file size as the array length
    #print("Length of data: " + str(len(arr)))

    HOST = 'localhost'
    PORT = 50007

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(arr)
    print('Finished sending swap File...')
    s.close()
    time.sleep(2)
    os.system('python Pc2.py')
    exit()



send(x+1)
