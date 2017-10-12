
class ExternalWeatherDataProviderNotInitialisedError(Exception):
    pass


class ExternalWeatherDataProviderBadAPIKey(Exception):

    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
