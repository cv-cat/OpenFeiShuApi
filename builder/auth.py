from utils.fly_book_utils import trans_cookies

class FlyBookAuth:
    def __init__(self):
        self.cookie = {}
        self.cookie_str = ''

    def perepare_auth(self, cookie_str: str):
        self.cookie = trans_cookies(cookie_str)
        self.cookie_str = cookie_str
