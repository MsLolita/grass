import json
import time
from base64 import b64decode, b64encode
from random import choice

from aiohttp import WSMsgType
import uuid


from core.utils.exception import WebsocketClosedException, ProxyForbiddenException

import os, base64

from data.config import NODE_TYPE


class GrassWs:
    def __init__(self, user_agent: str = None, proxy: str = None):
        self.user_agent = user_agent
        self.proxy = proxy

        self.session = None
        self.websocket = None
        self.id = None
        # self.ws_session = None

    async def connect(self):
        # self.proxy=None # testing on local network
        connection_port = ["4444", "4650"]
        uri = f"wss://proxy2.wynd.network:{choice(connection_port)}/"

        random_bytes = os.urandom(16)
        sec_websocket_key = base64.b64encode(random_bytes).decode('utf-8')

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-WebSocket-Key': sec_websocket_key,
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

        return json.loads(msg.data)

    async def get_connection_id(self):
        msg = await self.receive_message()
        return msg['id']

    async def auth_to_extension(self, browser_id: str, user_id: str):
        connection_id = await self.get_connection_id()

        message = {
            "id": connection_id,
            "origin_action": "AUTH",
            "result": {
                "browser_id": browser_id,
                "user_id": user_id,
                "user_agent": self.user_agent,
                "timestamp": int(time.time()),
                "device_type": "extension",
                "version": "4.26.2",
                "extension_id": "ilehaonighjijnmpnagapkhpcdbhclfg"
            }
        }

        if NODE_TYPE == "1_25x":
            message['result'].update({
                "extension_id": "lkbnfiajjmbhnfledhphioinpickokdi",
            })
        elif NODE_TYPE == "2x":
            message['result'].update({
                "device_type": "desktop",
                "version": "4.28.2",
            })
            message['result'].pop("extension_id")

        await self.send_message(json.dumps(message))

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

    async def handle_http_request_action(self):
        http_info = await self.receive_message()
        result = await self.build_http_request(http_info['data'])

        message = json.dumps(
            {
                "id": http_info["id"],
                "origin_action": "HTTP_REQUEST",
                "result": result
            }
        )

        await self.send_message(message)

    async def build_http_request(self, request_data):
        method = request_data['method']
        url = request_data['url']
        headers = request_data['headers']
        body = request_data.get("body")  # there may be no body

        if body:
            body = b64decode(
                body)  # this will probably be in json format when decoded but i dont think there is a need to turn it to a json

        try:
            response = await self.session.request(method, url,
                                                  headers=headers, data=body, proxy=self.proxy)

            if response:
                response.raise_for_status()
                response_headers_raw = response.headers
                response_headers = dict(response_headers_raw)
                response_body = await response.content.read()
                status_reason = response.reason
                status_code = response.status
                encoded_body = b64encode(response_body)
                encoded_body_as_str = encoded_body.decode('utf-8')
                return {
                    "body": encoded_body_as_str,
                    "headers": response_headers,
                    "status": status_code,
                    "status_text": status_reason,
                    "url": url
                }

        except Exception as e:
            # return this if anything happened
            return {}  # return an empty string if we have issues running the request
