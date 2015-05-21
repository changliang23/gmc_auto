import os
import urllib, urllib2
import ConfigParser
import paramiko
import time
import base64
import traceback
import gemslog

from bs4 import BeautifulSoup

__configfile = r"configuration\configuration.ini"
__autoitfile = r"setup\configure.ini"

def checkwebsitevalid(timeout):
    url = __getConfigurationValue("Setup", "dashboard")
    error = ""
    for i in range(1, timeout):
        time.sleep(1)
        try:
            page = urllib2.urlopen(url)
            if((str)(page.read()).find("Login")>0):
                return "True", ""
        except Exception, strerror:
            error = strerror.message.lower()
    return "False", __stringToBase64(error)

def changeBuildUrl(url):
    error = ''
    rt = 'True'
    try:
        url = "http://" + __base64ToString(url)
        __setConfigurationValue("Setup", "BuildRemoteUrl", url)
    except Exception, strerror:
        error = strerror.message.lower()
        rt = 'False'
    finally:
        return rt, __stringToBase64(error)

def config_autoit(fields):
    error = ''
    rt = 'True'
    try:
        #lyncversion, dbserver, dbname, dbport, username, password
        fields = __base64ToString(fields)
        params = fields.split("\n")
        __setUpdateConfigurationValue("InstallParameters","lyncversion",params[0])
        __setUpdateConfigurationValue("InstallParameters","db_server",params[1])
        __setUpdateConfigurationValue("InstallParameters","db_name",params[2])
        __setUpdateConfigurationValue("InstallParameters","db_port",params[3])
        __setUpdateConfigurationValue("InstallParameters","username",params[4])
        __setUpdateConfigurationValue("InstallParameters","password",params[5])
    except Exception, strerror:
        error = strerror.message.lower()
        rt = 'False'
    finally:
        return rt, __stringToBase64(error)

def download_windows_build():
    rt = 'True'
    error = ''
    try:
        special_build_file_name = __get_special_build()
        localPath = __getConfigurationValue("Setup", "BuildLocalPath")
        if len(special_build_file_name) > 0:
            if(os.path.exists(localPath + special_build_file_name)):
                os.remove(localPath + special_build_file_name)
            os.rename(__getConfigurationValue("Setup", "specialfolder") + '\\' + special_build_file_name, localPath + special_build_file_name)
            if(os.path.exists(__getConfigurationValue("Setup", "specialfolder") + '\\' + special_build_file_name)):
                os.remove(__getConfigurationValue("Setup", "specialfolder") + '\\' + special_build_file_name)
            __setUpdateConfigurationValue("Installer", "File", localPath + special_build_file_name)
    except Exception as e:
        error = str(e)
        rt = 'False'
        print traceback.format_exc()
    finally:
        return rt, __stringToBase64(error)

def changeInstallType(type):
    __setUpdateConfigurationValue("Type", "Type", type)
    return True, __stringToBase64("")

def install():
    return runBuild("Install")

def uninstall():
    return runBuild("Uninstall")

def upgrade():
    return runBuild("Upgrade")

def downgrade():
    return runBuild("Downgrade")

def runBuild(type):
    error = ''
    try:
        os.popen(r"taskkill /f /im Firefox.exe")
        os.popen(r"taskkill /f /im Iexplore.exe")
        os.popen(r"taskkill /f /im chrome.exe")
        __setUpdateConfigurationValue("Type", "Type", type)
        time.sleep(3)
        os.system(r'C:\autoinstall\cgi-bin\autoit.bat')
        time.sleep(20)
        rt = 'True'
    except Exception, strerror:
        error = strerror.message.lower()
        rt = 'False'
    finally:
        return rt, __stringToBase64(error)

def execute_karaf_command(cmd):
    client = paramiko.SSHClient()
    rt = "True"
    result = ""
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('127.0.0.1', 8101, username='admin', password='admin', timeout=20)
        line = __base64ToString(cmd)
        print line
        stdin, stdout, stderr = client.exec_command(line)
        for std in stdout.readlines():
            result = result + std + '\n'
    except Exception, strerror:
        result = strerror.strerror.lower()
        rt = "False"
    finally:
        client.close()
        return rt, __stringToBase64(result)

def get_install_log():
    rt = 'True'
    data = ''
    try:
        f = open(r'C:\Users\svcgmmadmin\AppData\Local\GoodServerInstallerLog.txt')
        for line in f.readlines():
            data = data + line
        f.close()
    except Exception, strerror:
        rt = 'False'
        data = str(strerror)
    finally:
        return rt, __stringToBase64(data)

def dump_gems_install_log():
    rt = 'True'
    data = 'copy gems install log success'
    src = r'C:\Users\svcgmmadmin\AppData\Local\GoodServerInstallerLog.txt'
    dst = r'C:\SpecialBuild\GoodServerInstallerLog.txt'
    try:
        if os.path.exists(dst):
            os.remove(dst)
        if os.path.exists(src):
            srcfile = file(src, 'r+')
            dstfile = file(dst, 'w+')
            dstfile.writelines(srcfile.read())
            srcfile.close()
            dstfile.close()
    except Exception, strerror:
        rt = 'False'
        data = str(strerror)
    finally:
        return rt, __stringToBase64(data)

def get_computer_name():
    rt = 'True'
    name = ''
    try:
        name = os.getenv('computername')
    except Exception, strerror:
        rt = 'False'
        name = strerror.message.lower()
    finally:
        return rt, __stringToBase64(name)

def console_remove_gems():
    if __check_gems_exists():
        s = os.system("msiexec /x " + __get_gems_uninstall_package() + " /passive /forcerestart")
        return 'True', __stringToBase64("remove gems success")
    else:
        return 'True', __stringToBase64("none gems build can be found")

def zip_gems_log():
    return gemslog.gemslog().getlog()

def __getBasePath():
    path = os.path.abspath(os.path.dirname(__file__))
    path = path.replace("cgi-bin", "")
    return path

def __getConfigurationValue(section, field):
    config = ConfigParser.ConfigParser()
    config.read(__getBasePath() + __configfile)
    value = config.get(section, field)
    return value

def __setConfigurationValue(section, field, value):
    config = ConfigParser.ConfigParser()
    config.read(__getBasePath() + __configfile)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, field, value)
    f = open(__getBasePath() + __configfile, "w+")
    config.write(f)
    f.close

def __setUpdateConfigurationValue(section, field, value):
    config = ConfigParser.ConfigParser()
    config.read(__getBasePath() + __autoitfile)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, field, value)
    f = open(__getBasePath() + __autoitfile, "w+")
    config.write(f)
    f.close

def __get_special_build():
    path = __getConfigurationValue("Setup", "specialfolder")
    files = os.listdir(path)
    if(len(files) > 0):
        for f in files:
            if(os.path.isfile(path + '/' + f)):
                if(f.find("exe") > 0):
                    return f
    else:
        return ""

def __stringToBase64(string):
    #return string
    return base64.b64encode(string)

def __base64ToString(b64):
    #return b64
    return base64.b64decode(b64)

def __get_gems_uninstall_package():
    p = os.popen("wmic product where \"name='Good Enterprise Mobility Server'\" get LocalPackage /value")
    result = p.read()
    result = result.replace("\n", "").replace("\r", "")
    return str(result.split("=")[1])

def __check_gems_exists():
    p = os.popen("wmic product where \"name='Good Enterprise Mobility Server'\" get LocalPackage /value")
    result = p.read()
    result = result.replace("\n", "").replace("\r", "")
    if len(result) > 0:
        return True
    else:
        return False

def test():
    return execute_karaf_command('config:update;config:edit com.good.gcs.http.client.AsyncHttpClientFactoryImpl;property-set DisableSSLCertificateChecking true;config:update;')

#print download_windows_build()
#print console_remove_gems()
