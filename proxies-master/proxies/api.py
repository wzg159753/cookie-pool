# -*-coding:utf-8 -*-


from gevent import pywsgi
from gevent import monkey
monkey.patch_all()
from flask import Flask, g
import json

from schedule.db import RedisClient


app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        # g.redis = RedisClient()
        website = 'tianyancha'
        g.redis = RedisClient('accounts', website=website)
    return g.redis


@app.route('/')
def index():
    return '<h2>hello</h2>'


@app.route('/get/')
def get_proxy():
    """获取随机可用cookie"""
    conn = get_conn()
    result = json.dumps({'status': 'failure', 'info': ""})
    try:
        proxy = conn.random()
        result = json.dumps({'status': 'success', 'cookies': proxy})
    except Exception as e:
        result = json.dumps({'status': 'failure', 'info': e})
    finally:
        return result

@app.route('/getvip/')
def get_vip_proxy():
    """获取随机可用cookie"""
    conn = get_conn()
    result = json.dumps({'status': 'failure', 'info': ""})
    try:
        proxy = conn.get_vip_proxy()
        result = json.dumps({'status': 'success', 'cookies': proxy})
    except Exception as e:
        result = json.dumps({'status': 'failure', 'info': e})
    finally:
        return result

@app.route('/count/')
def get_count():
    """获取cookies总数"""
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    from werkzeug.debug import DebuggedApplication
    app.debug = True
    dapp = DebuggedApplication(app, evalex= True)
    server = pywsgi.WSGIServer(( '127.0.0.1', 5000), dapp)
    server.serve_forever()
