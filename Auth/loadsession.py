from asyncio.windows_events import NULL
import onedrivesdk_fork as onedrivesdk
import datetime

## Just loading in the essentials
client_id='9072f955-93dc-4814-8edf-3c061e83d08a'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
api_base_url='https://api.onedrive.com/v1.0/'
client = NULL
#####################################################

def loadSession(client, client_id, scopes, api_base_url):
    try:
        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(
            http_provider=http_provider,
            client_id=client_id,
            scopes=scopes)
        client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

        auth_provider.load_session()
        auth_provider.refresh_token()
        client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
        return True
    except:
        print('No session pickle!')
        return False

######################################################