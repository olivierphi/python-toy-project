
class ExternalWeatherDataProviderNotInitialisedError(Exception):
    pass


class ExternalWeatherDataProviderBadAPIKey(Exception):

    def __init__(self, api_key):
        super()
        self.api_key = api_key
