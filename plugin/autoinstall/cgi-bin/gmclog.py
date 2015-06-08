import os

class gmclog:
    def __init__(self):
        self.__karafparentpath=r"C:\Program Files (x86)\Good Technology\Good Mobile Control"

    def getlog(self):
        result = "True"
        error = ""
        try:
            logpath = self.__locatelogs()
            zippath = os.path.abspath(os.path.dirname(__file__))
            rt = os.system(zippath + r"\7za.exe a -tzip C:\SpecialBuild\gmclog.zip " + "\"" + logpath + "\"")
            if rt != 0:
                result = "False"
                error = "gmc logs can not be zip"
            else:
                result = "True"
        except Exception, strerror:
            result = "False"
            error = strerror.message.lower()
        finally:
            return result, error

    def __locatelogs(self):
        list = os.listdir(self.__karafparentpath)
        for line in list:
            filepath = os.path.join(self.__karafparentpath, line)
            if os.path.isdir(filepath):
                currentpath = filepath + "\\log"
                break
        print "currentpath= " + currentpath
        return currentpath
