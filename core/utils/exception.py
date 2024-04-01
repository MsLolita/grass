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
