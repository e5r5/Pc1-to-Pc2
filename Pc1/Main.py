import threading
import os

def MyThread1():
    os.system('python GUI.py')
    #execfile(' GUI.py')

def MyThread2():
    os.system('python Wave.py')


global t1, t2
t1 = threading.Thread(target=MyThread1, args=[])
t2 = threading.Thread(target=MyThread2, args=[])


def startProg():
    t2.start()
    t1.start()


def StopAll():
    if(t1.is_alive):
        t1.daemon = True
    t2.daemon = True
    #exit()

if __name__=="__main__":
    startProg()

