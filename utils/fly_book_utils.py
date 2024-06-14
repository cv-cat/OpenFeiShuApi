import json
import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs

try:
    fly_book_js = execjs.compile(open(r'../static/fly_book.js', 'r', encoding='utf-8').read())
except:
    fly_book_js = execjs.compile(open(r'static/fly_book.js', 'r', encoding='utf-8').read())

def trans_cookies(cookies_str):
    cookies = dict()
    for i in cookies_str.split("; "):
        try:
            cookies[i.split('=')[0]] = '='.join(i.split('=')[1:])
        except:
            continue
    return cookies


def generate_access_key(mystr):
    access_key = fly_book_js.call('generate_access_key', mystr)
    return access_key

def generate_request_id():
    request_id = fly_book_js.call('generate_request_id')
    return request_id


def generate_long_request_id():
    request_id = fly_book_js.call('generate_long_request_id')
    return request_id

def generate_request_cid():
    request_cid = fly_book_js.call('generate_request_cid')
    return request_cid

