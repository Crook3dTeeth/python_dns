import dns
import os
import shutil


#Local file version
localVersion = dns.get_version()
newFile = 'C:/Users/tomkr/Documents/PythonDNS/python_dns/MainServer/newFile.py'

# NAS FILES
pathToFiles = 'Z:/dns.py'

try:
    try:
        shutil.copyfile(pathToFiles, newFile)
    except:
        raise Exception("ERROR: Failed to copy file")
    try:
        pass
    except:
        raise Exception("ERROR: Failed to import new version")

    try:
        oldVersion = dns.get_version()
        newVersion = newFile.get_version()
    except:
        raise Exception("ERROR: Failed to get version")

except Exception as ex:
    print(ex)