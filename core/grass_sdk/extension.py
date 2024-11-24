import json
import time
from random import choice

from aiohttp import WSMsgType

import uuid

from core.utils.exception import WebsocketClosedException, ProxyForbiddenException
from base64 import b64decode,b64encode
from core.utils import logger
class GrassWs:
    def __init__(self, user_agent: str = None, proxy: str = None):
        self.user_agent = user_agent
        self.proxy = proxy

        self.session = None
        self.websocket = None
        self.id = None
        self.ws_session = None

    async def connect(self):
        #self.proxy=None # testing on my local network will remove
        connection_port = ["4444", "4650"]
        uri = f"wss://proxy2.wynd.network:{choice(connection_port)}/"

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-WebSocket-Key': '94BKvjUp/+zImAvhNQWT3w==',
            'User-Agent': self.user_agent,
            'Upgrade': 'websocket',
            'Cache-Control': 'no-cache',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Version': '13',
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        }

        try:
            self.websocket = await self.ws_session.ws_connect(uri, proxy_headers=headers, proxy=self.proxy)
        except Exception as e:
            if 'status' in dir(e) and e.status == 403:
                raise ProxyForbiddenException(f"Low proxy score. Can't connect. Error: {e}")
            raise e

    async def send_message(self, message):
        #logger.info(f"Sending: {message}")
        await self.websocket.send_str(message)

    async def receive_message(self):
        msg = await self.websocket.receive()
        #logger.info(f"Received: {msg}")

        if msg.type == WSMsgType.CLOSED:
            raise WebsocketClosedException(f"Websocket closed: {msg}")
        msg_as_json=json.loads(msg.data)
        #logger.info(f"received {msg_as_json}")
        return msg_as_json

    async def auth_to_extension(self,connection_id, browser_id: str, user_id: str):

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
                    "version": "4.26.2",
                    "extension_id": "lkbnfiajjmbhnfledhphioinpickokdi"
                }
            }
        )

        await self.send_message(message)
    async def send_ping(self):
         send_message = json.dumps(
                    {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
         await self.send_message(send_message)

      
    async def send_pong(self,connection_id):
        message = json.dumps(
            {"id": connection_id, "origin_action": "PONG"}
        )

        await self.send_message(message)
   
    async def handle_http_action(self,msg):
        request_data = msg.get("data") # get the data
        result = await self.do_http_request(request_data)
        new_msg=json.dumps({"id": msg.get("id"), "origin_action": "HTTP_REQUEST", "result": result})
        #logger.info(f"HTTP request response {new_msg}")
        await self.send_message(new_msg)
                        
                        
    async def do_http_request(self,request_data):
        # credit to https://github.com/FungY911/better-grass for providing the inspiration for processing http requests
        method = request_data.get("method")
        url = request_data.get("url")
        headers = request_data.get("headers", {})
        body = request_data.get("body") # there may be no body
        if body: # if there is a body decode it
            body=b64decode(body) # this will probably be in json format when decoded but i dont think there is a need to turn it to a json
        try:
            
            response = await self.session.request(method,url, headers=headers, data=body,proxy=self.proxy)
            if response:
                response.raise_for_status()
                response_headers_raw=response.headers.multi_items()
                response_headers=dict(response_headers_raw)
                response_body=response.content
                status_reason=response.reason
                status_code=response.status_code
                encoded_body=b64encode(response_body)
                encoded_body_as_str = encoded_body.decode('utf-8')
                
                return{
                    "body":encoded_body_as_str,
                    "headers":response_headers,
                    "status":status_code,
                    "status_text":status_reason,
                    "url":url
                }
                
        except Exception as e:
            # return this if anything happened
            return{} # return an empty string if we havew issues running the request