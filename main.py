# Stupid workaround because python can't see the folder with the module
import sys
sys.path.append(".//Authentication")

from Authentication import ObjOneDrive

client = ObjOneDrive.clientObjectOneDrive('http://localhost:8080/', 'bQx7Q~j3mLZVVbJJrGbBOn6vmXs~EkV2dBYUU', 
            '9072f955-93dc-4814-8edf-3c061e83d08a', 'https://api.onedrive.com/v1.0/',
            ['wl.signin', 'wl.offline_access', 'onedrive.readwrite'])
client.auth()
client.printWorkDir()
client.ls()
client.navigate('New Folder')
client.navigate('y')
client.previousDir()
x = 1