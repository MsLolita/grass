import aiohttp


class WebsocketClosedException(Exception):
    pass


class ProxyError(Exception):
    pass


class LowProxyScoreException(ProxyError):
    pass


class ProxyScoreNotFoundException(ProxyError):
    pass


class ProxyForbiddenException(ProxyError):
    pass


class ConnectionException(aiohttp.ClientConnectionError):
    pass


class LoginException(Exception):
    pass


class WebsocketConnectionFailedError(Exception):
    pass


class FailureLimitReachedException(Exception):
    pass


class NoProxiesException(Exception):
    pass


class ProxyBlockedException(Exception):
    pass


class SiteIsDownException(Exception):
    pass


class EmailApproveLinkNotFoundException(Exception):
    pass


class RegistrationException(Exception):
    pass

class CloudFlareHtmlException(Exception):
    pass
