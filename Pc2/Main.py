import threading
import os

def MyThread1():
    os.system('python GUI.py')
    #execfile(' GUI.py')

def MyThread2():
    os.system('python Wave.py')

def MyThread3():
    print " "

def startProg():
    global t1,t2,t3
    t1 = threading.Thread(target=MyThread1, args=[])
    t2 = threading.Thread(target=MyThread2, args=[])
    t3 = threading.Thread(target=MyThread3, args=[])
   # t2.start()
    t1.start()
    t3.start()

def StopAll():
    global t1, t2, t3
    t1.exit()
    t2.exit()
    os.exit()

if __name__=="__main__":
    startProg()

