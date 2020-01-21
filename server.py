from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi
from utils import *
import re


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        config_id = re.sub("[^0-9]", "", self.path)
        try:
            name = self.server.configs[config_id][0]
            value = self.server.configs[config_id][1]
            self._set_headers()
            config = {'id': config_id, 'name': name, 'value': value}
            config = bytes(json.dumps(config), 'utf-8')
            self.wfile.write(config)
        except KeyError:
            # Send message back
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(NO_SUCH_ID_ERROR, encoding='utf-8'))
            return

    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype = cgi.parse_header(self.headers['Content-Type'])[0]

        # Refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # Read the message and convert it into a python dictionary
        length = int(self.headers['Content-Length'])
        message = json.loads(json.loads(self.rfile.read(length)))

        # Elaborate the request
        config_id = message['id']
        if config_id not in self.server.configs.keys():
            name = message['name']
            config = message['value']
            self.server.configs[config_id] = [name, config]

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("Success!", encoding='utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(ALREADY_ID_ERROR, encoding='utf-8'))
            return

    def do_PUT(self):
        ctype = cgi.parse_header(self.headers['Content-Type'])[0]

        # Refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # Read the message and convert it into a python dictionary
        length = int(self.headers['Content-Length'])
        message = json.loads(json.loads(self.rfile.read(length)))

        # Elaborate the request
        config_id = message['id']
        if config_id in self.server.configs.keys():
            name = message['name']
            config = message['value']
            self.server.configs[config_id] = [name, config]

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(OPERATION_SUCCESSFUL, encoding='utf-8'))
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(NO_SUCH_ID_ERROR, encoding='utf-8'))
            return

    def do_DELETE(self):
        config_id = re.sub("[^0-9]", "", self.path)
        try:
            del self.server.configs[config_id]

            # Send message back
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(OPERATION_SUCCESSFUL, encoding='utf-8'))
        except KeyError:
            # Send message back
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(NO_SUCH_ID_ERROR, encoding='utf-8'))
            return


class MyServer(HTTPServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address=server_address, RequestHandlerClass=handler_class)
        self.configs = {}


def run(port=PORT, server_class=MyServer, handler_class=MyHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % PORT)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
