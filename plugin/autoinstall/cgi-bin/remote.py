import cgi
import base64
from actions import *


print 'Content-Type: text/html\n\n'
#print '<h1>remote run successfully</h1>'


form = cgi.FieldStorage()
command = form['command'].value

if command == "setupcheck":
    result, data = 'setupcheck()'
elif command == "downloadbuild":
    result, data = download_windows_build()
elif command == "install":
    result, data = install()
elif command == "uninstall":
    result, data = uninstall()
elif command == "upgrade":
    result, data = upgrade()
elif command == "downgrade":
    result, data = downgrade()
elif command == 'getinstalllog':
    result, data = get_install_log()
elif command == 'dumpgemsinstalllog':
    result, data = dump_gems_install_log()
elif command == "configAutoIT":
    result, data = config_autoit((form['fields'].value))
elif command == "changeinstalltype":
    result, data = changeInstallType((form['type'].value))
elif command == "checkwebsitevalid":
    result, data = checkwebsitevalid((int)(form['timeout'].value))
elif command == "changeBuildUrl":
    result, data = changeBuildUrl((form['url'].value))
elif command == "karaf":
    result, data = execute_karaf_command(form['cmd'].value)
elif command == "computername":
    result, data = get_computer_name()
elif command == "removegemsbyconsole":
    result, data = console_remove_gems()
elif command == "zipgemslog":
    result, data = zip_gems_log()
elif command == "checkonline":
    result = "True"
    data = ""

print "<div style='color:#F00'>Test Result:</div>"
print "<div><result>" + result + "</result></div>"
print "<div>Return Data (Base64):</div>"
print "<div><data>" + data + "</data></div>"
