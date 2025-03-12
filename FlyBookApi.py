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
    cookie_str = 'passport_web_did=7425617429685633026; passport_trace_id=7425617429688434716; QXV0aHpDb250ZXh0=d0d5bf75e4ee4a1187352ee075c0371c; _gcl_au=1.1.7129592.1728911286; __tea__ug__uid=7425617339360134692; is_anonymous_session=; _csrf_token=a6cbc25b6f3327626935ed3aa0716af322963785-1728911297; lang=zh; session=XN0YXJ0-536qb617-01c6-4b41-853c-9e67e63a5822-WVuZA; session_list=XN0YXJ0-536qb617-01c6-4b41-853c-9e67e63a5822-WVuZA; sl_session=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzAyMzUxNjcsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdXQng5WkZBY0FCWkdSTnI2aExRQUpuRFJlMXJseUFBbWNORjdXdVhJQUNadzBYdjgyR1FBTUNLZ0VBUVVGQlFVRkJRVUZCUVVKdVNVdEtaa3gwUVVGQmR6MDkiLCJzdW0iOiJlOTdkOTVkYThhZDJkZGY5NGFkZGI1MjZkZWJjYzQ3ZWIwNjVjNGNiNmUwYTMwOTcxMmZhOTRiNmUyOTU4MmZlIiwibG9jIjoiemhfY24iLCJhcGMiOiIiLCJpYXQiOjE3MzAxOTE5NjcsInNhYyI6eyJVc2VyU3RhZmZTdGF0dXMiOiIxIiwiVXNlclR5cGUiOiI0MiJ9LCJsb2QiOm51bGwsIm5zIjoibGFyayIsIm5zX3VpZCI6IjczMTQzNDY5OTI5MjEwNjc1MjEiLCJuc190aWQiOiI3MjMzOTkyMzE4MzAxOTc4NjI2Iiwib3QiOjF9fQ.goZHVVubY2mjX4jWaO1lPkfpSGZ1Y_-SaZuG-w0bnpl_omBplJfk2_zZbbDUsmhWhgErL3BFFZopPM81Ov2v5g; site_env=pre=0; _uuid_hera_ab_path_1=7431117940350795778; landing_url=https://www.feishu.cn/download; Hm_lvt_a79616d9322d81f12a92402ac6ae32ea=1730191974; HMACCOUNT=75F4600EFAF92CE2; _gid=GA1.2.1889448621.1730191975; help_center_session=9cd28d94-0690-4914-bb66-bbc7d50518e2; _uetsid=2fcd8bd095d311efb6d2adb31009996d; _uetvid=2fcdcaf095d311ef9cebe166df088ce7; Hm_lpvt_a79616d9322d81f12a92402ac6ae32ea=1730191977; _ga_VPYRHN104D=GS1.1.1730191974.2.1.1730191976.58.0.0; _ga=GA1.2.104448125.1728911286; i18n_locale=zh-CN; locale=zh-CN; passport_app_access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzAyMzUxODIsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjEiOnsiaWF0IjoxNzMwMTkxOTgyLCJhY2Nlc3MiOnRydWV9fSwic3VtIjoiZTk3ZDk1ZGE4YWQyZGRmOTRhZGRiNTI2ZGViY2M0N2ViMDY1YzRjYjZlMGEzMDk3MTJmYTk0YjZlMjk1ODJmZSJ9fQ.Ax5t58BcfEjIONiePYpUaD0FoSdfH_lIcf0UI02YwYeoEmjBy4peGF71AQ82qj83f45urVSLB7zFtJiND-tczA; swp_csrf_token=39ce677f-fd7e-452c-b5fb-a6a621c57623; t_beda37=1e652d1a0a89f5aa215a96161e6762af794145b9dd2d1d78322e32587ba5aa1d; msToken=huib7ZvPSFnE4D22NUX6r82DSruVZG5JhhJHojihK7l00B8-B8XxJWY68jDnx11fV1GvSz0QuUU7N5RbYo8eyGQnZeKz0kDFwX-XfkaH6NI8-QVM1Rgpd8cdHGSSjMz7M_yugUdc_iWJeNV8S45uTbHomfsLrPwETJ_a83HELt6aaB5nbm_uwg=='
    fly_book_auth.perepare_auth(cookie_str)

    res_json, x_csrf_token = fly_book_api.get_csrf_token(fly_book_auth)
    res_json, userId = fly_book_api.get_user_info(fly_book_auth, x_csrf_token)
    # ========================================================================================================
    query = 'ShellBot'
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

    # sends_text = '测试消息'
    # # chatId = "7379910344918188035"
    # res = fly_book_api.send_msg(fly_book_auth, sends_text, chatId)
    # print(res)
