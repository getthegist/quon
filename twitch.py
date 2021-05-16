import requests

class Twitch():

    def __init__(self, client_id, bearer=None):
        self.client_id = client_id
        self.bearer = bearer

    def get_bearer(self, secret):
        url = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(self.client_id, secret)
        response = requests.post(url).json()
        access_token = response['access_token']
        self.bearer = access_token
        return(access_token)

    def get_stream_info (self, streamer_name):
        url = "https://api.twitch.tv/helix/search/channels?query={}&first=1".format(streamer_name)
        headers = {
                "Client-Id": self.client_id,
                "Authorization": "Bearer {}".format(self.bearer)
        }
        try:
            response = requests.get(url, headers=headers).json()
            data = response['data'][0]
        except:
            data = {"is_live": False}

        return data
