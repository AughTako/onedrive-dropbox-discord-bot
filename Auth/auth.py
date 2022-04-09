from asyncio.windows_events import NULL
import onedrivesdk_fork as onedrivesdk
import os

redirect_uri = 'http://localhost:8080/'
client_secret = 'bQx7Q~j3mLZVVbJJrGbBOn6vmXs~EkV2dBYUU'
client_id='9072f955-93dc-4814-8edf-3c061e83d08a'
api_base_url='https://api.onedrive.com/v1.0/'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

http_provider = onedrivesdk.HttpProvider()
auth_provider = onedrivesdk.AuthProvider(
    http_provider=http_provider,
    client_id=client_id,
    scopes=scopes)

def auth(client, auth_provider):
    try:
       #client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
        auth_url = client.auth_provider.get_auth_url(redirect_uri)
        # Ask for the code
        print('Paste this URL into your browser, approve the app\'s access.')
        print('Copy everything in the address bar after "code=", and paste it below.')
        print(auth_url)
        code = input('Paste code here: ')
        path = 'C:\\Users\\Nazgul\\Desktop\\OneDrive-DiscordBot\\session.pickle'
        if(not os.path.isfile(path)):
            print('No session pickle... Creating')
        client.auth_provider.authenticate(code, redirect_uri, client_secret)
        ### No need to ask for the code after the first launch ###
        auth_provider.save_session()
        auth_provider = onedrivesdk.AuthProvider(http_provider,
                                                client_id,
                                                scopes)
        auth_provider.load_session()
        auth_provider.refresh_token()
        client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
        print('@@@@ Session saved and refreshed! @@@@')
    except:
        print('Bad auth!')
