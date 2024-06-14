import json

import requests

from builder.auth import FlyBookAuth
from builder.header import HeaderBuilder
from builder.params import ParamsBuilder
from builder.proto import ProtoBuilder

class FlyBookApi:
    base_url = "https://internal-api-lark-api.feishu.cn/im/gateway/"
    get_csrf_token_url = "https://internal-api-lark-api.feishu.cn/accounts/csrf"
    get_user_info_url = "https://internal-api-lark-api.feishu.cn/accounts/web/user"
    def get_csrf_token(self, auth):
        headers = HeaderBuilder.build_get_csrf_token_header().get()
        params = ParamsBuilder.build_get_csrf_token_param().get()
        response = requests.post(self.get_csrf_token_url, headers=headers, cookies=auth.cookie, params=params, verify=False)
        res_json = response.json()
        x_csrf_token = response.cookies.get('swp_csrf_token')
        return res_json, x_csrf_token

    def get_user_info(self, auth, x_csrf_token):
        headers = HeaderBuilder.build_get_user_info_header(x_csrf_token).get()
        params = ParamsBuilder.build_get_user_info_param().get()
        response = requests.get(self.get_user_info_url, headers=headers, cookies=auth.cookie, params=params, verify=False)
        res_json = response.json()
        userId = res_json['data']['user']['id']
        return res_json, userId

    def search_some(self, auth, query):
        headers = HeaderBuilder.build_search_header().get()
        Packet = ProtoBuilder.build_search_request_proto(headers['x-request-id'], query)
        response = requests.post(self.base_url, headers=headers, cookies=auth.cookie, data=Packet.SerializeToString(), verify=False)
        SearchResponsePacket, userAndGroupIds = ProtoBuilder.decode_search_response_proto(response.content)
        return SearchResponsePacket, userAndGroupIds

    def create_chat(self, auth, userId):
        headers = HeaderBuilder.build_create_chat_header().get()
        Packet = ProtoBuilder.build_create_chat_request_proto(headers['x-request-id'], userId)
        response = requests.post(self.base_url, headers=headers, cookies=auth.cookie, data=Packet.SerializeToString(), verify=False)
        PutChatResponsePacket, chatId = ProtoBuilder.decode_create_chat_response_proto(response.content)
        return PutChatResponsePacket, chatId

    def send_msg(self, auth, sends_text, chatId):
        headers = HeaderBuilder.build_send_msg_header().get()
        Packet = ProtoBuilder.build_send_message_request_proto(sends_text, headers['x-request-id'], chatId)
        response = requests.post(self.base_url, headers=headers, cookies=auth.cookie, data=Packet.SerializeToString(), verify=False)
        return response.text



if __name__ == '__main__':
    fly_book_api = FlyBookApi()
    fly_book_auth = FlyBookAuth()
    cookie_str = ''
    cookie_str = 'passport_web_did=7360675712451543044; QXV0aHpDb250ZXh0=1e4557f7d39f4311aa4ea6bab7afb858; locale=zh-CN; _gcl_au=1.1.1773137480.1713790863; trust_browser_id=1078ea84-34d9-42d4-adff-766c423ab3e8; _ga=GA1.1.252483876.1713790863; is_anonymous_session=; _ga_VPYRHN104D=GS1.1.1713790863.1.1.1713790872.51.0.0; lang=zh; __tea__ug__uid=1007701713790873353; _uuid_hera_ab_path_1=7372781885275160579; Hm_lvt_e78c0cb1b97ef970304b53d2097845fd=1716609558; _csrf_token=36b375aad3381c672c2752df4c2f78c9bc1b51ae-1716787751; session=XN0YXJ0-8f0hd84c-4929-4782-8aa7-04633ae72d3c-WVuZA; session_list=XN0YXJ0-8f0hd84c-4929-4782-8aa7-04633ae72d3c-WVuZA_XN0YXJ0-cbcu2232-bd07-4258-ba84-bd690f3f3b9a-WVuZA; msToken=1aL_Z6EfXm8A5YvLxai6CT2XUrk4rk-TS1Tr9VEIqx5dwdqXD_raGfMXYFZPQr3B_aVm00bKlLyYQ6fw2u-BHADiWT81bCZ2Vfft2Dm0_AzIVT8PUcoBPjUu0STE1Q==; swp_csrf_token=5b7a9c24-5b0e-4a21-aac5-d14df211b626; t_beda37=69b2049004fece16b30d54b3358913eaa94b3bc0773542938c79503a8a4d7908; passport_app_access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgzODY1NjQsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjEiOnsiaWF0IjoxNzE4MzQzMzY0LCJhY2Nlc3MiOnRydWV9fSwic3VtIjoiYWFmOWZjOGNkN2MzMDZjOTZiMTM3YzJiYmJjNjQ3OGM0NmY2MmJjYWQxZGQ1OTM4OGMwYmFkZDk4Njk2ZTA4OCJ9fQ.7VFjobyga9-3a2CRmNOQ32jE7jJvFVApZnkf2iHMKm-b_CCz1rFCfqD9YVKXsQhIV87RzZ0w8dQB3m_4VadwSg; sl_session=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgzODkyMjIsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdXQng5WkZBY0FCWkdSTnI2aExRQUptSmwrUDI0VUFCR1ltWDQvYmhRQUVaaVpmbWRDSVFBTUNLZ0VBUVVGQlFVRkJRVUZCUVVKdFdtRkxaRXBSVWtGQmR6MDkiLCJzdW0iOiJhYWY5ZmM4Y2Q3YzMwNmM5NmIxMzdjMmJiYmM2NDc4YzQ2ZjYyYmNhZDFkZDU5Mzg4YzBiYWRkOTg2OTZlMDg4IiwibG9jIjoiemhfY24iLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzE4MzQ2MDIyLCJzYWMiOnsiVXNlclN0YWZmU3RhdHVzIjoiMSIsIlVzZXJUeXBlIjoiNDIifSwibG9kIjpudWxsLCJucyI6ImxhcmsiLCJuc191aWQiOiI3MzE0MzQ2OTkyOTIxMDY3NTIxIiwibnNfdGlkIjoiNzIzMzk5MjMxODMwMTk3ODYyNiIsIm90IjoxfX0.CejevDo3dkcdhkj_dhEDfyB0SkUTbuhwlLJY8Enx6ystjcqMOmD9X09rBaaHCmWFs2_sio4RejcIc0_kKGkcGQ'
    fly_book_auth.perepare_auth(cookie_str)

    res_json, x_csrf_token = fly_book_api.get_csrf_token(fly_book_auth)
    res_json, userId = fly_book_api.get_user_info(fly_book_auth, x_csrf_token)
    # ========================================================================================================
    query = 'NoraSpider-PD'
    SearchResponsePacket, userAndGroupIds = fly_book_api.search_some(fly_book_auth, query)
    user_or_group_id = userAndGroupIds[0]
    if user_or_group_id['type'] == 'user':
        print('搜索到用户')
        userId = user_or_group_id['id']
        PutChatResponsePacket, chatId = fly_book_api.create_chat(fly_book_auth, userId)
        # print(chatId)
    else:
        print('搜索到群组')
        chatId = user_or_group_id['id']

    # ========================================================================================================
    # userId = "7355149382943080450"
    # PutChatResponsePacket, chatId = fly_book_api.create_chat(fly_book_auth, userId)
    # print(chatId)

    sends_text = 'Group,test'
    # chatId = "7379910344918188035"
    res = fly_book_api.send_msg(fly_book_auth, sends_text, chatId)
    print(res)
