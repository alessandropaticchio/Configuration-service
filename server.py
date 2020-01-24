from utils import *
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi
import psycopg2
from socketserver import ThreadingMixIn

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
        '''
        Method to handle GET requests at URL: http://localhost:PORT/?{ID}. It accomplishes the task to read the
        configurations from the service, knowing its ID.
        '''
        # Get ID from the request path
        config_id = self.path[2:]

        connection_db, cursor = self.connect_to_DB()

        # Lock acquire
        cursor.execute('SELECT pg_advisory_lock({})'.format(LOCK_ID))

        with connection_db:
            cursor.execute('SELECT * FROM configuration WHERE id=%s', (config_id,))
            res = cursor.fetchall()

        if len(res) != 0:
            # Fetch data and create a dictionary to send to the client
            name, value = res[0][1], res[0][2]
            config = {'id': config_id, 'name': name, 'value': value}
            response_code = 200
            content_type = 'application/json'
            answer = config
        else:
            # Send error message back
            response_code=400
            content_type='text/plain'
            answer = NO_SUCH_ID_ERROR

        # Lock release
        cursor.execute('SELECT pg_advisory_unlock({})'.format(LOCK_ID))

        self.reply(response_code=response_code, content_type=content_type, answer=answer)

    # POST echoes the message adding a JSON field
    def do_POST(self):
        '''
        Method to handle POST requests at URL: http://localhost:PORT, whose Content-Type is 'application/json'
        and has a JSON object in the body. It accomplishes the task to create new configurations in the service.

        JSON Object example:
        {
	        "id" : "a", "name" : "b", "value" : "c"
        }
        '''
        c_type = cgi.parse_header(self.headers['Content-Type'])[0]

        # Refuse to receive non-json content
        if c_type != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # Read the message and convert it into a python dictionary
        length = int(self.headers['Content-Length'])
        message = self.rfile.read(length).decode('utf-8')
        message = json.loads(message)

        if type(message) == str:
            message = json.loads(message)

        # Elaborate the request
        config_id = message['id']

        connection_db, cursor = self.connect_to_DB()

        content_type = 'text/plain'

        try:
            with connection_db:
                name = message['name']
                value = message['value']

                # Lock acquire
                cursor.execute('SELECT pg_try_advisory_lock({})'.format(LOCK_ID))

                cursor.execute('INSERT into configuration(id, name, value) VALUES(%s,%s,%s)', (config_id,
                                                                                                name,
                                                                                                value))

                # Lock release
                cursor.execute('SELECT pg_advisory_unlock({})'.format(LOCK_ID))

                response_code = 200
                answer = OPERATION_SUCCESSFUL
                self.reply(response_code=response_code, content_type=content_type, answer=answer)
        except psycopg2.errors.UniqueViolation:
            # Send error message back
            response_code = 400
            answer = ALREADY_ID_ERROR
            self.reply(response_code=response_code, content_type=content_type, answer=answer)


    def do_PUT(self):
        '''
        Method to handle PUT requests at URL: http://localhost:PORT, whose Content-Type is 'application/json'
        and has a JSON object in the body. It accomplishes the task to update existing configuration in the service.

        JSON Object example:
        {
	        "id" : "a", "name" : "b", "value" : "c"
        }
        '''
        c_type = cgi.parse_header(self.headers['Content-Type'])[0]

        # Refuse to receive non-json content
        if c_type != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # Read the message and convert it into a python dictionary
        length = int(self.headers['Content-Length'])
        message = json.loads(self.rfile.read(length))

        if type(message) == str:
            message = json.loads(message)

        # Connect to DB
        connection_db, cursor = self.connect_to_DB()

        # Elaborate the request
        config_id = message['id']

        with connection_db:
            # Add the updated config to the DB
            name = message['name']
            value = message['value']

            # Lock acquire
            cursor.execute('SELECT pg_try_advisory_lock({})'.format(LOCK_ID))

            # Check if the config to update exists
            cursor.execute('SELECT * FROM configuration WHERE id=%s', (config_id,))
            res = cursor.fetchall()

            # If the config to update exists, the operation is done. Otherwise an error message is sent back
            if len(res) != 0:
                cursor.execute('UPDATE configuration SET name=%s, value=%s WHERE id=%s', (name, value, config_id))
                response_code = 200
                answer = OPERATION_SUCCESSFUL
            else:
                # Send error message back
                response_code = 400
                answer = NO_SUCH_ID_ERROR

            # Lock release
            cursor.execute('SELECT pg_advisory_unlock({})'.format(LOCK_ID))

            content_type = 'text/plain'
            self.reply(response_code=response_code, content_type=content_type, answer=answer)

    def do_DELETE(self):
        '''
        Method to handle DELETE requests at URL: http://localhost:PORT/?{ID}. It accomplishes the task to delete an
        existing configuration in the service, knowing its ID.
        '''
        # Get ID from the request path
        config_id = self.path[2:]

        # Connect to DB
        connection_db, cursor = self.connect_to_DB()

        with connection_db:

            # Lock acquire
            cursor.execute('SELECT pg_advisory_lock({})'.format(LOCK_ID))

            # Check if the config to delete exists
            cursor.execute('SELECT * FROM configuration WHERE id=%s', (config_id, ))
            res = cursor.fetchall()

            # If the config to delete exists, the operation is done. Otherwise an error message is sent back
            if len(res) != 0:
                cursor.execute('DELETE FROM configuration WHERE id=%s', (config_id,))
                response_code = 200
                answer = OPERATION_SUCCESSFUL
            else:
                # Send error message back
                response_code = 400
                answer = NO_SUCH_ID_ERROR

            # Lock release
            cursor.execute('SELECT pg_advisory_unlock({})'.format(LOCK_ID))

            content_type = 'text/plain'
            self.reply(response_code=response_code, content_type=content_type, answer=answer)

    @staticmethod
    def connect_to_DB():

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


class MyServer(ThreadingMixIn, HTTPServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address=server_address, RequestHandlerClass=handler_class)
        self.KEEP_ALIVE = True

    def run(self):
        while self.KEEP_ALIVE:
            self.handle_request()


if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = MyServer(server_address, MyHandler)

    print('Starting configuration service on port %d...' % PORT)
    httpd.run()