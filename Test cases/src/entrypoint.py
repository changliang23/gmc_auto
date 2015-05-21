__author__ = 'Gavinliu'
import sys
import os
from robot.utils import asserts

class EntryPoint:
    def __init__(self):
        sys.path.append(os.path.abspath(os.path.dirname(__file__)))

    def execute(self, command, action, *values):
        #print 'execute(' + command + "," + action + ")"
        module = __import__(command)
        cls = getattr(module, command)
        clsObj = cls()
        method = getattr(clsObj, action)
        if(len(values)==0):
            return method()
        elif(len(values)==1):
            return method(values[0])
        elif(len(values)==2):
            return method(values[0],values[1])
        elif(len(values)==3):
            return method(values[0],values[1],values[2])
        elif(len(values)==4):
            return method(values[0],values[1],values[2],values[3])
        elif(len(values)==5):
            return method(values[0],values[1],values[2],values[3],values[4])
        elif(len(values)==6):
            return method(values[0],values[1],values[2],values[3],values[4],values[5])
        elif(len(values)==7):
            return method(values[0],values[1],values[2],values[3],values[4],values[5],values[6])

def Execute(command, action, *values):
    ep = EntryPoint()
    print 'Execute(' + command + "," + action + ")"
    if(len(values)==0):
        result, error = ep.execute(command, action)
    elif(len(values)==1):
        result, error = ep.execute(command, action, values[0])
    elif(len(values)==2):
        result, error = ep.execute(command, action, values[0],values[1])
    elif(len(values)==3):
        result, error = ep.execute(command, action, values[0],values[1],values[2])
    elif(len(values)==4):
        result, error = ep.execute(command, action, values[0],values[1],values[2],values[3])
    elif(len(values)==5):
        result, error = ep.execute(command, action, values[0],values[1],values[2],values[3],values[4])
    elif(len(values)==6):
        result, error = ep.execute(command, action, values[0],values[1],values[2],values[3],values[4],values[5])
    elif(len(values)==7):
        result, error = ep.execute(command, action, values[0],values[1],values[2],values[3],values[4],values[5],values[6])
    return (str)(result),error

def should_be_more_than_as_integer(source, baseline):
    if(source>=baseline):
        asserts.assert_true(True,"Expected: source>=baseline" + " (source=" + (str)(source)  + ", baseline=" + (str)(baseline) + ")")
    else:
        asserts.assert_false(True,"Expected: source>=baseline" + " (source=" + (str)(source)  + ", baseline=" + (str)(baseline) + ")")

def kill_Driver():
    os.popen(r"taskkill /f /im Firefox.exe")
    os.popen(r"taskkill /f /im Iexplore.exe")
    os.popen(r"taskkill /f /im chrome.exe")
    os.popen(r"taskkill /f /im IEDriverServer.exe")
    os.popen(r"taskkill /f /im chromedriver.exe")

