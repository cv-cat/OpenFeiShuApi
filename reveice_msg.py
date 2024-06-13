from urllib.parse import urlencode

from websocket import WebSocketApp
import static.proto_pb2 as FLY_BOOK_PROTO
from FlyBookApi import FlyBookApi

from builder.auth import FlyBookAuth
from builder.params import ParamsBuilder
from builder.proto import ProtoBuilder


class FlyBookLive:
    def __init__(self):
        self.ws = None

    @staticmethod
    def on_message(ws, message):
        try:
            Frame, Packet_sid, fromId, ChatId, ReceiveTextContent = ProtoBuilder.decode_receive_msg_proto(message)
            print(Frame)

            if ChatId is not None:
                print(f"fromId: {fromId}")
                print(f"ChatId: {ChatId}")
                print(f"ReceiveTextContent: {ReceiveTextContent}")

                if not fromId == '7314346992921067521':
                    fly_book_api = FlyBookApi()
                    fly_book_auth = FlyBookAuth()
                    cookie_str = 'passport_web_did=7360675712451543044; QXV0aHpDb250ZXh0=1e4557f7d39f4311aa4ea6bab7afb858; locale=zh-CN; _gcl_au=1.1.1773137480.1713790863; trust_browser_id=1078ea84-34d9-42d4-adff-766c423ab3e8; _ga=GA1.1.252483876.1713790863; is_anonymous_session=; _ga_VPYRHN104D=GS1.1.1713790863.1.1.1713790872.51.0.0; lang=zh; __tea__ug__uid=1007701713790873353; _uuid_hera_ab_path_1=7372781885275160579; Hm_lvt_e78c0cb1b97ef970304b53d2097845fd=1716609558; _csrf_token=36b375aad3381c672c2752df4c2f78c9bc1b51ae-1716787751; session=XN0YXJ0-8f0hd84c-4929-4782-8aa7-04633ae72d3c-WVuZA; session_list=XN0YXJ0-8f0hd84c-4929-4782-8aa7-04633ae72d3c-WVuZA_XN0YXJ0-cbcu2232-bd07-4258-ba84-bd690f3f3b9a-WVuZA; passport_app_access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgyMzcyMTIsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjEiOnsiaWF0IjoxNzE4MTk0MDEyLCJhY2Nlc3MiOnRydWV9fSwic3VtIjoiYWFmOWZjOGNkN2MzMDZjOTZiMTM3YzJiYmJjNjQ3OGM0NmY2MmJjYWQxZGQ1OTM4OGMwYmFkZDk4Njk2ZTA4OCJ9fQ.VevkzfsmJZN-ETiSEOx6ciNJNdNrT1ipRVyu_AKhVkODXIzMnr96mGbdga8gwcDvurJYv0F8QXCnXi6URJPi6A; sl_session=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgyMzg3NzYsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdXQng5WkZBY0FCWkdSTnI2aExRQUptSmwrUDI0VUFCR1ltWDQvYmhRQUVaaVpmbWRDSVFBTUNLZ0VBUVVGQlFVRkJRVUZCUVVKdFdtRkxaRXBSVWtGQmR6MDkiLCJzdW0iOiJhYWY5ZmM4Y2Q3YzMwNmM5NmIxMzdjMmJiYmM2NDc4YzQ2ZjYyYmNhZDFkZDU5Mzg4YzBiYWRkOTg2OTZlMDg4IiwibG9jIjoiemhfY24iLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzE4MTk1NTc2LCJzYWMiOnsiVXNlclN0YWZmU3RhdHVzIjoiMSIsIlVzZXJUeXBlIjoiNDIifSwibG9kIjpudWxsLCJucyI6ImxhcmsiLCJuc191aWQiOiI3MzE0MzQ2OTkyOTIxMDY3NTIxIiwibnNfdGlkIjoiNzIzMzk5MjMxODMwMTk3ODYyNiIsIm90IjoxfX0.KyqL8o8buuFFWBfurekxIlV2mhNZuvBEmUdyD2FjQ5kQc3RmjqlnxPe2g2Mh9HPUaBi31rILaW9NNsPyeDZKHA; swp_csrf_token=06b39a70-8d22-40fb-9d86-a39aecc2a1b6; t_beda37=23d411157af861afbc9c1bf6032b116898bb57702b61c0c8e7ac536df6d7ccec'
                    fly_book_auth.perepare_auth(cookie_str)
                    sends_text = ReceiveTextContent
                    res = fly_book_api.send_msg(fly_book_auth, sends_text, ChatId)
                    print(res)


            sends = FLY_BOOK_PROTO.Packet()
            sends.cmd = 1
            sends.payloadType = 1
            sends.sid = Packet_sid
            s = sends.SerializeToString()
            ws.send(s, opcode=0x2)
            print('==============================')
        except Exception as e:
            print(str(e))

    @staticmethod
    def on_error(ws, error):
        print("\033[31m### error ###")
        print(error)
        print("### ===error=== ###\033[m")

    @staticmethod
    def on_close(ws, close_status_code, close_msg):
        print("\033[31m### closed ###")
        print(f"status_code: {close_status_code}, msg: {close_msg}")
        print("### ===closed=== ###\033[m")

    def start_ws(self, wss_url):
        self.ws = WebSocketApp(
            url=wss_url,
            on_message=FlyBookLive.on_message,
            on_error=FlyBookLive.on_error,
            on_close=FlyBookLive.on_close
        )
        try:
            self.ws.run_forever()
        except Exception as e:
            print(str(e))
            self.ws.close()


if __name__ == '__main__':
    live = FlyBookLive()
    fly_book_auth = FlyBookAuth()
    cookie_str = 'passport_web_did=7360675712451543044; QXV0aHpDb250ZXh0=1e4557f7d39f4311aa4ea6bab7afb858; locale=zh-CN; _gcl_au=1.1.1773137480.1713790863; trust_browser_id=1078ea84-34d9-42d4-adff-766c423ab3e8; _ga=GA1.1.252483876.1713790863; is_anonymous_session=; _ga_VPYRHN104D=GS1.1.1713790863.1.1.1713790872.51.0.0; lang=zh; __tea__ug__uid=1007701713790873353; _uuid_hera_ab_path_1=7372781885275160579; Hm_lvt_e78c0cb1b97ef970304b53d2097845fd=1716609558; _csrf_token=36b375aad3381c672c2752df4c2f78c9bc1b51ae-1716787751; session=XN0YXJ0-8f0hd84c-4929-4782-8aa7-04633ae72d3c-WVuZA; session_list=XN0YXJ0-8f0hd84c-4929-4782-8aa7-04633ae72d3c-WVuZA_XN0YXJ0-cbcu2232-bd07-4258-ba84-bd690f3f3b9a-WVuZA; passport_app_access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgyMzcyMTIsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjEiOnsiaWF0IjoxNzE4MTk0MDEyLCJhY2Nlc3MiOnRydWV9fSwic3VtIjoiYWFmOWZjOGNkN2MzMDZjOTZiMTM3YzJiYmJjNjQ3OGM0NmY2MmJjYWQxZGQ1OTM4OGMwYmFkZDk4Njk2ZTA4OCJ9fQ.VevkzfsmJZN-ETiSEOx6ciNJNdNrT1ipRVyu_AKhVkODXIzMnr96mGbdga8gwcDvurJYv0F8QXCnXi6URJPi6A; sl_session=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgyMzg3NzYsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdXQng5WkZBY0FCWkdSTnI2aExRQUptSmwrUDI0VUFCR1ltWDQvYmhRQUVaaVpmbWRDSVFBTUNLZ0VBUVVGQlFVRkJRVUZCUVVKdFdtRkxaRXBSVWtGQmR6MDkiLCJzdW0iOiJhYWY5ZmM4Y2Q3YzMwNmM5NmIxMzdjMmJiYmM2NDc4YzQ2ZjYyYmNhZDFkZDU5Mzg4YzBiYWRkOTg2OTZlMDg4IiwibG9jIjoiemhfY24iLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzE4MTk1NTc2LCJzYWMiOnsiVXNlclN0YWZmU3RhdHVzIjoiMSIsIlVzZXJUeXBlIjoiNDIifSwibG9kIjpudWxsLCJucyI6ImxhcmsiLCJuc191aWQiOiI3MzE0MzQ2OTkyOTIxMDY3NTIxIiwibnNfdGlkIjoiNzIzMzk5MjMxODMwMTk3ODYyNiIsIm90IjoxfX0.KyqL8o8buuFFWBfurekxIlV2mhNZuvBEmUdyD2FjQ5kQc3RmjqlnxPe2g2Mh9HPUaBi31rILaW9NNsPyeDZKHA; swp_csrf_token=06b39a70-8d22-40fb-9d86-a39aecc2a1b6; t_beda37=23d411157af861afbc9c1bf6032b116898bb57702b61c0c8e7ac536df6d7ccec'
    fly_book_auth.perepare_auth(cookie_str)
    params = ParamsBuilder.build_receive_msg_param(fly_book_auth).get()
    url = f"wss://msg-frontier.feishu.cn/ws/v2?{urlencode(params)}"
    live.start_ws(url)