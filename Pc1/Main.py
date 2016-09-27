import threading
import os

def MyThread1():
    os.system('python GUI.py')
    #execfile(' GUI.py')

def MyThread2():
    os.system('python Wave.py')

def MyThread3():
    print " "


global t1, t2, t3
t1 = threading.Thread(target=MyThread1, args=[])
t2 = threading.Thread(target=MyThread2, args=[])
t3 = threading.Thread(target=MyThread3, args=[])

def startProg():
    t2.start()
    t1.start()
    t3.start()

def StopAll():
    if(t1.is_alive):
        t1.daemon = True
    t2.daemon = True
    #exit()

if __name__=="__main__":
    startProg()

