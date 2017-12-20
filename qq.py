from multiprocessing import Process
import sys

rocket = 0

def func1():
    global rocket
    print ('start func1')
    while rocket < 1000:
        print('f1 '+str(rocket))
        rocket += 1
    print ('end func1')

def func2():
    global rocket
    print ('start func2')
    while rocket < 1000:
        print ('f2 '+str(rocket))
        rocket += 1
    print ('end func2')

if __name__=='__main__':
    p1 = Process(target=func1)
    p1.start()
    p2 = Process(target=func2)
    p2.start()
