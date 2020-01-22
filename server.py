from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi
from utils import *
import psycopg2


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def reply(self, response_code, content_type, answer):
        self.send_response(response_code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if content_type == 'application/json':
            # Convert from dict to json and send it to the client
            answer = json.dumps(answer)
        self.wfile.write(bytes(answer, encoding='utf-8'))

    def do_GET(self):

        # Get ID from the request path
        config_id = self.path[2:]

        connection_db, cursor = self.connect_to_DB()

        with connection_db:
            cursor.execute('SELECT * FROM configuration WHERE id=%s', (config_id,))
            res = cursor.fetchall()

        if len(res) != 0:
            # Fetch data and create a dictionary to send to the client
            name, value = res[0][1], res[0][2]
            config = {'id': config_id, 'name': name, 'value': value}
            self.reply(response_code=200, content_type='application/json', answer=config)
        else:
            # Send error message back
            self.reply(response_code=400, content_type='text/plain', answer=NO_SUCH_ID_ERROR)
            return

    # POST echoes the message adding a JSON field
    def do_POST(self):
        c_type = cgi.parse_header(self.headers['Content-Type'])[0]

        # Refuse to receive non-json content
        if c_type != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # Read the message and convert it into a python dictionary
        length = int(self.headers['Content-Length'])
        # message = json.loads(json.loads(self.rfile.read(length)))
        message = json.loads(json.loads(self.rfile.read(length).decode('utf-8')))

        # Elaborate the request
        config_id = message['id']

        connection_db, cursor = self.connect_to_DB()

        try:
            with connection_db:
                name = message['name']
                value = message['value']

                cursor.execute('INSERT into configuration(id, name, value) VALUES(%s,%s,%s)', (config_id,
                                                                                                name,
                                                                                                value))

                self.reply(response_code=200, content_type='text/plain', answer=OPERATION_SUCCESSFUL)
        except psycopg2.errors.UniqueViolation:
            # Send error message back
             self.reply(response_code=400, content_type='text/plain', answer=ALREADY_ID_ERROR)


    def do_PUT(self):
        c_type = cgi.parse_header(self.headers['Content-Type'])[0]

        # Refuse to receive non-json content
        if c_type != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # Read the message and convert it into a python dictionary
        length = int(self.headers['Content-Length'])
        message = json.loads(json.loads(self.rfile.read(length)))

        # Connect to DB
        connection_db, cursor = self.connect_to_DB()

        # Elaborate the request
        config_id = message['id']

        with connection_db:
            # Add the updated config to the DB
            name = message['name']
            value = message['value']

            # Check if the config to update exists
            cursor.execute('SELECT * FROM configuration WHERE id=%s', (config_id,))
            res = cursor.fetchall()

            # If the config to update exists, the operation is done. Otherwise an error message is sent back
            if len(res) != 0:
                cursor.execute('UPDATE configuration SET name=%s, value=%s WHERE id=%s', (name, value, config_id))
                self.reply(response_code=200, content_type='text/plain', answer=OPERATION_SUCCESSFUL)
            else:
                # Send error message back
                self.reply(response_code=400, content_type='text/plain', answer=NO_SUCH_ID_ERROR)

    def do_DELETE(self):
        # Get ID from the request path
        config_id = self.path[2:]

        # Connect to DB
        connection_db, cursor = self.connect_to_DB()

        with connection_db:

            # Check if the config to delete exists
            cursor.execute('SELECT * FROM configuration WHERE id=%s', (config_id, ))
            res = cursor.fetchall()

            # If the config to delete exists, the operation is done. Otherwise an error message is sent back
            if len(res) != 0:
                cursor.execute('DELETE FROM configuration WHERE id=%s', (config_id,))
                self.reply(response_code=200, content_type='text/plain', answer=OPERATION_SUCCESSFUL)
            else:
                # Send error message back
                self.reply(response_code=400, content_type='text/plain', answer=NO_SUCH_ID_ERROR)

    def connect_to_DB(self):

        # DB connection
        connection_db = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        cursor = connection_db.cursor()

        return connection_db, cursor


class MyServer(HTTPServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address=server_address, RequestHandlerClass=handler_class)


def run(port=PORT, server_class=MyServer, handler_class=MyHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting configuration server on port %d...' % PORT)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
