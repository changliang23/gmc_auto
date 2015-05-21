__author__ = 'gavinliu'
import ConfigParser
import os
import sys

class configuration():
    def __init__(self, ini=r'\config.ini'):
        sys.path.append(os.path.abspath(os.path.dirname(__file__)))
        if(ini == r'\config.ini'):
            self.__inifile = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + ini
        else:
            self.__inifile = ini

    def getValue(self, section, field):
        config = ConfigParser.ConfigParser()
        config.read(self.__inifile)
        value = config.get(section, field)
        return value

    def setValue(self, section, field, value):
        config = ConfigParser.ConfigParser()
        config.read(self.__inifile)
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, field, value)
        f = open(self.__inifile, "w+")
        config.write(f)
        f.close

    def InitEnv(self):
        txt = ""
        rootdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        for parent, dirnames, filenames in os.walk(rootdir):
            for filename in filenames:
                if(filename.find("global_share_resource.txt") != -1):
                    txt = os.path.join(parent, filename)
        if(len(txt)>0):
            return self.__replaceTxtFile(txt)
        else:
            return False

    def __replaceTxtFile(self, txt):
        file = open(txt)
        lines = []
        while 1:
            line = file.readline()
            if not line:
                break
            if(line.find(self.getValue("ConvertList", "DBConnectionString")) == 0 ):
                line = self.getValue("ConvertList", "DBConnectionString") + "    " + self.GetDBConnectionString() + "\n"
            elif(line.find(self.getValue("ConvertList", "DBInstance")) == 0 ):
                line = self.getValue("ConvertList", "DBInstance") + "    " + self.__getDBInstance() + "\n"
            elif(line.find(self.getValue("ConvertList", "DBName")) == 0 ):
                line = self.getValue("ConvertList", "DBName") + "    " + self.getValue("Database", "MasterDBName") + "\n"
            elif(line.find(self.getValue("ConvertList", "DBUser")) == 0 ):
                line = self.getValue("ConvertList", "DBUser") + "    " + self.getValue("Database", "MasterDBUser") + "\n"
            elif(line.find(self.getValue("ConvertList", "DBPwd")) == 0 ):
                line = self.getValue("ConvertList", "DBPwd") + "    " + self.getValue("Database", "MasterDBPwd") + "\n"
            elif(line.find(self.getValue("ConvertList", "GEMSUrl")) == 0 ):
                line = self.getValue("ConvertList", "GEMSUrl") + "    " + self.getValue("Server", "Server") + ":" + self.getValue("Server", "SSLPort") + "\n"
            elif(line.find(self.getValue("ConvertList", "GEMSServer")) == 0 ):
                line = self.getValue("ConvertList", "GEMSServer") + "    " + self.getValue("Server", "Server") + "\n"
            elif(line.find(self.getValue("ConvertList", "GEMSUser")) == 0 ):
                line = self.getValue("ConvertList", "GEMSUser") + "    " + self.getValue("Server", "Domain") + "\\" + self.getValue("Server", "UserName") + "\n"
            elif(line.find(self.getValue("ConvertList", "GEMSLog")) == 0 ):
                line = self.getValue("ConvertList", "GEMSLog") + "    " + r'H:\\Program Files\\Good Technology\\Good Enterprise Mobility Server\\Good Server Distribution\\$karaf$\\data\\log\\' + "\n"
            elif(line.find(self.getValue("ConvertList", "dashboarduser")) == 0 ):
                line = self.getValue("ConvertList", "dashboarduser") + "    " + self.getValue("Server", "UserName") + "\n"
            elif(line.find(self.getValue("ConvertList", "dashboardpd")) == 0 ):
                line = self.getValue("ConvertList", "dashboardpd") + "    " + self.getValue("Server", "password") + "\n"
            elif(line.find(self.getValue("ConvertList", "browser")) ==0 ):
                line = self.getValue("ConvertList", "browser") + "    " + self.getValue("GEMS", "browser") + "\n"
            lines.append(line)

        file.close()
        file = open(txt,'w')
        file.close()
        file = open(txt, 'wt')
        file.writelines(lines)
        file.close()
        return True

    def GetDBConnectionString(self):
        instance = ""
        if(len(self.getValue("Database","MasterDBInstance"))>0):
            instance = r"\\" + self.getValue("Database", "MasterDBInstance")
        dbstr = r"DRIVER={SQL Server};SERVER=" + \
                self.getValue("Database", "MasterDBIp") + instance + \
                ";DATABASE=" + self.getValue("Database", "MasterDBName") + \
                ";UID=" + self.getValue("Database", "MasterDBUser") + \
                ";PWD=" + self.getValue("Database", "MasterDBPwd")
        return dbstr

    def ReturnDBConnectionString(self):
        instance = ""
        if(len(self.getValue("Database","MasterDBInstance"))>0):
            instance = "\\" + self.getValue("Database", "MasterDBInstance")
        dbstr = r"DRIVER={SQL Server};SERVER=" + \
                self.getValue("Database", "MasterDBIp") + instance + \
                ";DATABASE=" + self.getValue("Database", "MasterDBName") + \
                ";UID=" + self.getValue("Database", "MasterDBUser") + \
                ";PWD=" + self.getValue("Database", "MasterDBPwd")
        return dbstr

    def GetGEMSLogString(self):
        return self.getValue("GEMSOnpremiss","logfilepath")

    def __getDBInstance(self):
        if(len(self.getValue("Database","MasterDBInstance")) > 0):
            return self.getValue("Database", "MasterDBIp") + r"\\" + self.getValue("Database", "MasterDBInstance")
        else:
            return self.getValue("Database", "MasterDBIp")

    def GetAutoITDBInstance(self):
        if(len(self.getValue("Database","MasterDBInstance")) > 0):
            return self.getValue("Database", "MasterDBIp") + "\\" + self.getValue("Database", "MasterDBInstance")
        else:
            return self.getValue("Database", "MasterDBIp")

    def GetWebLink(self):
        web_link = self.getValue("Server","Server") + ":" + self.getValue("Server","SSLPort")
        return web_link

    def LoadCheckpointFileByKey(self, key):
        filepath = os.path.abspath(os.path.dirname(__file__)) + "\\CheckPoint\\" + self.getValue("GEMSLogCheckPoint", key)
        result = []
        with open(filepath, 'r') as f:
            for line in f:
                result.append(line.strip('\n'))
        return result
