from http.server import BaseHTTPRequestHandler, HTTPServer # python3

import threading
import json
import socket
import requests

class HttpRequestModelInfoServer():
    scene_model =  None
    def __init__(self, scene_model, animator, camera_matrix, configs):
        self.animator = animator
        self.camera_matrix = camera_matrix

        HttpRequestModelInfoServer.scene_model = scene_model
        with open('config.json', 'r') as f:
            configs = json.loads(f.read())
        self.addr = (configs['get_info']['address'], configs['get_info']['port'])

        self.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(3600)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.listen(5)

        self.thread = Thread(scene_model, self.addr[0], self.addr[1], self.sock)
        self.thread.start()

    def close(self):
        print('closing http server')
        self.sock.close()
        self.thread.keep_running = False
        print('Done!')

class Thread(threading.Thread):
    def __init__(self, scene_model, host, port, sock):
        self.scene_model = scene_model
        self.host = host
        self.port = port
        self.sock = sock
        self.keep_running = True
        super(Thread, self).__init__(target=self.run)

    def run(self):
        self.httpd = HTTPServer((self.host, self.port), MyHttpHandler, False)

        # Prevent the HTTP server from re-binding every handler.
        # https://stackoverflow.com/questions/46210672/
        self.httpd.socket = self.sock
        self.httpd.server_bind = self.server_close = lambda self: None
        while self.keep_running:
            self.httpd.handle_request()



class MyHttpHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(bytes(res, 'utf-8'))

    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        rcp = json.loads(post_body)['request']

        if rcp == 'get_alive_utxos':
            res = str([u.index for u in HttpRequestModelInfoServer.scene_model.getAliveUtxos()])
        else:
            res = 'rcp not recognised'

        self._set_headers()
        self.wfile.write(bytes(res, 'utf-8'))

    def do_PUT(self):
        self._set_headers()
        print("received put request")
        self.wfile.write(bytes("received post request", 'utf-8'))

