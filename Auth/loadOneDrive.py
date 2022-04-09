from asyncio.windows_events import NULL
import loadsession
import auth
import onedrivesdk_fork as onedrivesdk

client_id='9072f955-93dc-4814-8edf-3c061e83d08a'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
api_base_url='https://api.onedrive.com/v1.0/'
http_provider = onedrivesdk.HttpProvider()
auth_provider = onedrivesdk.AuthProvider(
    http_provider=http_provider,
    client_id=client_id,
    scopes=scopes)
client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)
def LoadAPI():
    if(loadsession.loadSession(client, client_id, scopes, api_base_url)):
        print('Session pickle loaded!')
    else:
        auth.auth(client, auth_provider)

