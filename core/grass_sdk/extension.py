import json
import time

from aiohttp import WSMsgType

import uuid

from core.utils.exception import WebsocketClosedException, ProxyForbiddenException


class GrassWs:
    def __init__(self, user_agent: str = None, proxy: str = None):
        self.user_agent = user_agent
        self.proxy = proxy

        self.session = None
        self.websocket = None
        self.id = None

    async def connect(self):
        uri = "wss://proxy.wynd.network:4444/"

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'chrome-extension://ilehaonighjijnmpnagapkhpcdbhclfg',
            'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': self.user_agent,
            'Upgrade': 'websocket',
            'Cache-Control': 'no-cache',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Version': '13',
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        }
        try:
            self.websocket = await self.session.ws_connect(uri, proxy_headers=headers, proxy=self.proxy)
        except Exception as e:
            if 'status' in dir(e) and e.status == 403:
                raise ProxyForbiddenException(f"Low proxy score. Can't connect. Error: {e}")
            raise e

    async def send_message(self, message):
        # logger.info(f"Sending: {message}")
        await self.websocket.send_str(message)

    async def receive_message(self):
        msg = await self.websocket.receive()
        # logger.info(f"Received: {msg}")

        if msg.type == WSMsgType.CLOSED:
            raise WebsocketClosedException(f"Websocket closed: {msg}")

        return msg.data

    async def get_connection_id(self):
        msg = await self.receive_message()
        return json.loads(msg)['id']

    async def auth_to_extension(self, browser_id: str, user_id: str):
        connection_id = await self.get_connection_id()

        message = json.dumps(
            {
                "id": connection_id,
                "origin_action": "AUTH",
                "result": {
                    "browser_id": browser_id,
                    "user_id": user_id,
                    "user_agent": self.user_agent,
                    "timestamp": int(time.time()),
                    "device_type": "extension",
                    "version": "3.3.2"
                }
            }
        )

        await self.send_message(message)

    async def send_ping(self):
        message = json.dumps(
            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}}
        )

        await self.send_message(message)

    async def send_pong(self):
        connection_id = await self.get_connection_id()

        message = json.dumps(
            {"id": connection_id, "origin_action": "PONG"}
        )

        await self.send_message(message)
