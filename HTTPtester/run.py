# -*- coding: utf-8 -*-

from HTTPtester import app

if __name__ == '__main__':
    host = "127.0.0.1"
    port = 5000
    debug = True
    app.run(host, port, debug=debug)

