from asyncio.windows_events import NULL
from gc import collect
from json import load
from unicodedata import name
import onedrivesdk_fork as onedrivesdk
import os

class clientObjectOneDrive:
    redirect_uri = '' #= 'http://localhost:8080/'
    client_secret = ''# = 'bQx7Q~j3mLZVVbJJrGbBOn6vmXs~EkV2dBYUU'
    client_id = ''#'9072f955-93dc-4814-8edf-3c061e83d08a'
    api_base_url = '' #'https://api.onedrive.com/v1.0/'
    scopes = [] #['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
    client = NULL
    currDir = NULL
    collectionIds = []
    pathTo = ['root']
    def __init__(self, r_url, client_s, client_id, api_url, scopes):
        self.redirect_uri = r_url
        self.client_secret = client_s
        self.client_id = client_id
        self.api_base_url = api_url
        self.scopes = scopes
    def auth(self):
        try:
            path = '.\\session.pickle'
            if(not os.path.isfile(path)):
                print('No session pickle... Creating')
                http_provider = onedrivesdk.HttpProvider()
                auth_provider = onedrivesdk.AuthProvider(
                    http_provider=http_provider,
                    client_id= self.client_id,
                    scopes= self.scopes)
                client = onedrivesdk.OneDriveClient(self.api_base_url, auth_provider, http_provider)
                auth_url = client.auth_provider.get_auth_url('http://localhost:8080/')
                # Ask for the code
                print('Paste this URL into your browser, approve the app\'s access.')
                print('Copy everything in the address bar after "code=", and paste it below.')
                print(auth_url)
                code = input('Paste code here: ')
                client.auth_provider.authenticate(code, self.redirect_uri, self.client_secret)
                ### No need to ask for the code after the first launch ###
                auth_provider.save_session()
                auth_provider = onedrivesdk.AuthProvider(http_provider,
                                                        self.client_id,
                                                        self.scopes)
                auth_provider.load_session()
                auth_provider.refresh_token()
                self.client = onedrivesdk.OneDriveClient(self.api_base_url, auth_provider, http_provider)
                self.currDir = self.client.item(path = './')
                print('@@@@ Session saved and refreshed! @@@@')
            else:
                self.loadSession()
        except:
            print('Bad auth!')
    """
    Kind of self-explanitory; loadSession just loads the pickle that's stored locally,
    while the auth() method does the first-time authorization and when it doesn't go through
    it raises an exception and prints.
    """
    def loadSession(self):
        try:
            http_provider = onedrivesdk.HttpProvider()
            auth_provider = onedrivesdk.AuthProvider(
                http_provider=http_provider,
                client_id= self.client_id,
                scopes= self.scopes)
            client = onedrivesdk.OneDriveClient(self.api_base_url, auth_provider, http_provider)

            auth_provider.load_session()
            auth_provider.refresh_token()
            self.client = onedrivesdk.OneDriveClient(self.api_base_url, auth_provider, http_provider)
            self.currDir = self.client.item(path = './')
            print('Loaded session!')
        except:
            print('Bad session!')
    
    def printWorkDir(self):
        if(self.pathTo[0] == 'root'):
            self.pathTo.remove('root')
        print('root/', end = '')
        for item in self.pathTo:
            print(item.name + '/' , end='')
        print(end = '\n')
        
    def ls(self):
        collection = self.currDir.children.request().get()
        for items in collection:
            print(items.name, ' ID:', items.id)
            self.collectionIds.append(items.id)

    def navigate(self, item_name): 
        item_id = ''
        collection = self.currDir.children.request().get()
        for items in collection:
            if(items.name == item_name):
                item_id = items.id
        self.collectionIds.clear()
        print('####################################')
        print('Navigating to directory => ', self.client.item(id = item_id).get().name)
        self.pathTo.append(self.client.item(id = item_id).get())
        print('Current directory path is: ', end = '') 
        self.printWorkDir()
        print('####################################')
        self.currDir = (self.client).item(id = item_id)
        self.ls()        

    def previousDir(self):
        self.pathTo.pop()
        self.currDir = (self.client).item(id = self.pathTo[len(self.pathTo) - 1].id)
        self.collectionIds.clear()
        collection = self.currDir.children.request().get()
        print('####################################')
        print('Navigating up one level!')
        print('Current directory path is: ', end = '') 
        self.printWorkDir()
        print('####################################')
        for items in collection:
            self.collectionIds.append(items.id)
        self.ls()