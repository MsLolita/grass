import asyncio
import json
import time
from base64 import b64encode
from aiohttp import WSMsgType
import uuid

from better_proxy import Proxy

from core.utils.exception import WebsocketClosedException, ProxyForbiddenException, ProxyError

import os, base64

from data.config import NODE_TYPE


class GrassWs:
    def __init__(self, user_agent: str = None, proxy: str = None):
        self.user_agent = user_agent
        self.proxy = proxy
        self.destination = None
        self.token = None
        self.session = None
        self.websocket = None
        self.id = None
        # self.ws_session = None

    async def get_addr(self, browser_id: str, user_id: str):
        EXTENSION_ID_1x = "ilehaonighjijnmpnagapkhpcdbhclfg"
        EXTENSION_ID_1_25x = "lkbnfiajjmbhnfledhphioinpickokdi"

        message = {
            "browserId": browser_id,
            "userId": user_id,
            "version": "5.1.1",
            "extensionId": EXTENSION_ID_1x,
            "userAgent": self.user_agent,
            "deviceType": "extension"
        }

        headers = {
            'Connection': 'keep-alive',
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Origin': f'chrome-extension://{EXTENSION_ID_1x}',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Storage-Access': 'active',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US;q=0.8,en;q=0.7',
        }


        if NODE_TYPE == "1_25x" :
            message["extension_id"] = EXTENSION_ID_1_25x
            headers['Origin'] = f'chrome-extension://{EXTENSION_ID_1_25x}'
        elif NODE_TYPE == "2x":
            message["extension_id"] = EXTENSION_ID_1_25x
            headers['Origin'] = f'chrome-extension://{EXTENSION_ID_1_25x}'

        try:
            response = await self.session.post(
                'https://director.getgrass.io/checkin',
                json=message,
                headers=headers,
                proxy=self.proxy,
                ssl=False
            )

            if response.status == 201:
                try:
                    text = await response.text()
                    try:
                        data = json.loads(text)
                    except json.JSONDecodeError as e:
                        print(f"Received non-JSON response: {text}")
                        raise ProxyError(f"Received non-JSON response: {text}")

                    self.destination = data.get('destinations')[0] if data.get('destinations') else None
                    self.token = data.get('token')

                    if not self.destination:
                        raise ProxyError("No destination received")

                    return self.destination, self.token
                except Exception as e:
                    print(f"Error processing response: {e}, response: {response.status}")
                    raise ProxyError(f"Error processing response: {e}")
            else:
                print(f"Failed to get connection info: {response.status}")
                raise ProxyError(f"Failed to get connection info: {response.status}")

        except Exception as e:
            print(f"Error getting connection info: {type(e).__name__}: {e}")
            raise ProxyError(f"Error getting connection info: {type(e).__name__}: {e}")

    async def connect(self):
        uri = f"wss://{self.destination}/?token={self.token}"

        random_bytes = os.urandom(16)
        sec_websocket_key = base64.b64encode(random_bytes).decode('utf-8')

        headers = {
            'Host': self.destination,
            'Connection': 'Upgrade',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'User-Agent': self.user_agent,
            'Upgrade': 'websocket',
            'Origin': 'chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi',
            'Sec-WebSocket-Version': '13',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-WebSocket-Key': sec_websocket_key,
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
            'Accept': ''
        }

        try:
            self.websocket = await self.session.ws_connect(
                uri,
                headers=headers,
                proxy=self.proxy,
                ssl=True
            )

        except Exception as e:
            if 'status' in dir(e) and e.status == 403:
                raise ProxyForbiddenException(f"Low proxy score. Can't connect. Error: {e}")
            raise e

    async def send_message(self, message):
        await self.websocket.send_str(message)

    async def receive_message(self):
        msg = await self.websocket.receive()
        if msg.type == WSMsgType.CLOSED:
            raise WebsocketClosedException(f"Websocket closed: {msg}")
        return json.loads(msg.data)

    async def get_connection_id(self):
        return await self.receive_message()

    async def action_extension(self):
        received_message = await self.get_connection_id()
        message_id = received_message.get("id")
        action = received_message.get("action")
        data = received_message.get("data", {})

        response = {
            "id": message_id,
            "origin_action": action
        }

        if action == "HTTP_REQUEST":
            result = await self.perform_http_request(data)

            response["result"] = result

        response_str = json.dumps(response, separators=(',', ':'))
        await self.send_message(response_str)

    async def perform_http_request(self, params: dict) -> dict:
        headers = params.get("headers", {})
        method = params.get("method", "GET")
        url = params["url"]
        body = params.get("body")

        try:
            async with self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=body,
                    proxy=self.proxy,
                    ssl=False
            ) as response:
                status = response.status
                status_text = response.reason
                headers_dict = dict(response.headers)

                body_bytes = await response.read()
                body_base64 = b64encode(body_bytes).decode('utf-8')

                return {
                    "url": str(response.url),
                    "status": status,
                    "status_text": status_text,
                    "headers": headers_dict,
                    "body": body_base64
                }
        except Exception as e:
            print(f"Error occurred while performing fetch: {e}")
            return {
                "url": url,
                "status": 400,
                "status_text": "Bad Request",
                "headers": {},
                "body": ""
            }

    async def send_ping(self):
        message = {
            "id": str(uuid.uuid4()),
            "version": "1.0.0",
            "action": "PING",
            "data": {}
        }
        message_str = json.dumps(message, separators=(',', ':'))
        await self.send_message(message_str)
