import re
import time
from urllib.parse import urlencode

import asyncio

import blackboxprotobuf
import static.proto_pb2 as FLY_BOOK_PROTO
from FlyBookApi import FlyBookApi
import websockets

from builder.auth import FlyBookAuth
from builder.params import ParamsBuilder
from builder.proto import ProtoBuilder


class FlyBookLive:
    def __init__(self, auth):
        self.base_url = 'wss://msg-frontier.feishu.cn/ws/v2'
        self.auth = auth
        self.fly_book_api = FlyBookApi()
        _, x_csrf_token = self.fly_book_api.get_csrf_token(self.auth)
        _, self.me_id = self.fly_book_api.get_user_info(self.auth, x_csrf_token)
        self.me_id = str(self.me_id)
        self.ws = None

    async def send_ack(self, ws, Packet_sid):
        payload = FLY_BOOK_PROTO.Packet()
        payload.cmd = 1
        payload.payloadType = 1
        payload.sid = Packet_sid
        payload = payload.SerializeToString()
        Frame = FLY_BOOK_PROTO.Frame()
        current = int(time.time() * 1000)
        Frame.seqid = current
        Frame.logid = current
        Frame.service = 1
        Frame.method = 1
        ExtendedEntry = FLY_BOOK_PROTO.ExtendedEntry()
        ExtendedEntry.key = 'x-request-time'
        ExtendedEntry.value = f'{current}000'
        Frame.headers.append(ExtendedEntry)
        Frame.payloadType = "pb"
        Frame.payload = payload
        Frame = Frame.SerializeToString()
        await ws.send(Frame)

    async def main(self):
        params = ParamsBuilder.build_receive_msg_param(auth).get()
        url = f"{self.base_url}?{urlencode(params)}"
        async with websockets.connect(url) as websocket:
            async for message in websocket:
                try:
                    Frame, Packet_sid, fromId, MessageChatId, ReceiveTextContent = ProtoBuilder.decode_receive_msg_proto(message)
                    if MessageChatId is not None:
                        print(f"fromId: {fromId}")
                        print(f"ChatId: {MessageChatId}")
                        print(f"ReceiveTextContent: {ReceiveTextContent}")
                        if not str(fromId) == self.me_id:
                            try:
                                if self.me_id in ReceiveTextContent:
                                    to_who = re.findall(r'给\$(.*?)\$', ReceiveTextContent)[0]
                                    send_text = re.findall(r'发送\$(.*?)\$', ReceiveTextContent)[0]
                                    _, userAndGroupIds = self.fly_book_api.search_some(self.auth, to_who)
                                    user_or_group_id = userAndGroupIds[0]
                                    if user_or_group_id['type'] == 'user':
                                        userId = user_or_group_id['id']
                                        _, chatId = self.fly_book_api.create_chat(self.auth, userId)
                                    else:
                                        chatId = user_or_group_id['id']
                                    self.fly_book_api.send_msg(self.auth, send_text, chatId)
                                else:
                                    raise Exception
                            except Exception as e:
                                pass
                                # send_text = '我是一个机器人，如果你想和我聊天，请@我并发送消息，消息格式：给$用户名$发送$消息内容$'
                                # self.fly_book_api.send_msg(self.auth, send_text, MessageChatId)

                    await self.send_ack(websocket, Packet_sid)
                    print('==============================')
                except Exception as e:
                    exception = str(e)
                    print(str(e))


if __name__ == '__main__':
    auth = FlyBookAuth()
    cookie_str = 'passport_web_did=7360675712451543044; QXV0aHpDb250ZXh0=1e4557f7d39f4311aa4ea6bab7afb858; locale=zh-CN; _gcl_au=1.1.1773137480.1713790863; trust_browser_id=1078ea84-34d9-42d4-adff-766c423ab3e8; _ga=GA1.1.252483876.1713790863; is_anonymous_session=; _ga_VPYRHN104D=GS1.1.1713790863.1.1.1713790872.51.0.0; lang=zh; __tea__ug__uid=1007701713790873353; _uuid_hera_ab_path_1=7372781885275160579; Hm_lvt_e78c0cb1b97ef970304b53d2097845fd=1716609558; _csrf_token=36b375aad3381c672c2752df4c2f78c9bc1b51ae-1716787751; session=XN0YXJ0-8f0hd84c-4929-4782-8aa7-04633ae72d3c-WVuZA; session_list=XN0YXJ0-8f0hd84c-4929-4782-8aa7-04633ae72d3c-WVuZA_XN0YXJ0-cbcu2232-bd07-4258-ba84-bd690f3f3b9a-WVuZA; passport_app_access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgyMzcyMTIsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjEiOnsiaWF0IjoxNzE4MTk0MDEyLCJhY2Nlc3MiOnRydWV9fSwic3VtIjoiYWFmOWZjOGNkN2MzMDZjOTZiMTM3YzJiYmJjNjQ3OGM0NmY2MmJjYWQxZGQ1OTM4OGMwYmFkZDk4Njk2ZTA4OCJ9fQ.VevkzfsmJZN-ETiSEOx6ciNJNdNrT1ipRVyu_AKhVkODXIzMnr96mGbdga8gwcDvurJYv0F8QXCnXi6URJPi6A; sl_session=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgyMzg3NzYsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdXQng5WkZBY0FCWkdSTnI2aExRQUptSmwrUDI0VUFCR1ltWDQvYmhRQUVaaVpmbWRDSVFBTUNLZ0VBUVVGQlFVRkJRVUZCUVVKdFdtRkxaRXBSVWtGQmR6MDkiLCJzdW0iOiJhYWY5ZmM4Y2Q3YzMwNmM5NmIxMzdjMmJiYmM2NDc4YzQ2ZjYyYmNhZDFkZDU5Mzg4YzBiYWRkOTg2OTZlMDg4IiwibG9jIjoiemhfY24iLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzE4MTk1NTc2LCJzYWMiOnsiVXNlclN0YWZmU3RhdHVzIjoiMSIsIlVzZXJUeXBlIjoiNDIifSwibG9kIjpudWxsLCJucyI6ImxhcmsiLCJuc191aWQiOiI3MzE0MzQ2OTkyOTIxMDY3NTIxIiwibnNfdGlkIjoiNzIzMzk5MjMxODMwMTk3ODYyNiIsIm90IjoxfX0.KyqL8o8buuFFWBfurekxIlV2mhNZuvBEmUdyD2FjQ5kQc3RmjqlnxPe2g2Mh9HPUaBi31rILaW9NNsPyeDZKHA; swp_csrf_token=06b39a70-8d22-40fb-9d86-a39aecc2a1b6; t_beda37=23d411157af861afbc9c1bf6032b116898bb57702b61c0c8e7ac536df6d7ccec'
    auth.perepare_auth(cookie_str)

    live = FlyBookLive(auth)
    asyncio.run(live.main())