from client import Client
from server import *
import threading

'''This file is used to test the integration between client and server. It tests that all the requests received
by the server are correctly processed'''

def create_new_config(test_client):
    '''
    Test if the creation of a new configuration actually inserts data in the database
    '''

    connection_db, cursor = MyHandler.connect_to_DB()

    with connection_db:
        test_client.craft_POST('create test 1 2', verbose=False)
        cursor.execute('SELECT * FROM configuration WHERE id=%s', ('test',))
        res = cursor.fetchall()
        assert res[0][0] == 'test'
        assert res[0][1] == '1'
        assert res[0][2] == '2'

        test_client.craft_DELETE('delete test', verbose=False)


def create_existing_config(test_client):
    '''
    Test if the creation of a new configuration does not insert data in the database
    '''

    connection_db, cursor = MyHandler.connect_to_DB()

    with connection_db:
        test_client.craft_POST('create test 1 2', verbose=False)
        test_client.craft_POST('create test 3 4', verbose=False)
        cursor.execute('SELECT * FROM configuration WHERE id=%s', ('test',))
        res = cursor.fetchall()
        assert res[0][0] == 'test'
        assert res[0][1] == '1'
        assert res[0][2] == '2'

        test_client.craft_DELETE('delete test', verbose=False)


def delete_existing_config(test_client):
    '''
    Test if the deletion of a new configuration eliminates data in the database
    '''

    connection_db, cursor = MyHandler.connect_to_DB()

    with connection_db:
        test_client.craft_POST('create test 1 2', verbose=False)
        test_client.craft_DELETE('delete test', verbose=False)
        cursor.execute('SELECT * FROM configuration WHERE id=%s', ('test',))
        res = cursor.fetchall()
        assert len(res) == 0
        test_client.craft_DELETE('delete test', verbose=False)


def delete_not_existing_config(test_client):
    '''
    Test if the deletion of a new configuration does not insert data in the database
    '''

    connection_db, cursor = MyHandler.connect_to_DB()

    with connection_db:
        test_client.craft_DELETE('delete not_existing', verbose=False)
        cursor.execute('SELECT * FROM configuration WHERE id=%s', ('not_existing',))
        res = cursor.fetchall()
        assert len(res) == 0

def update_existing_config(test_client):
    '''
    Test if the update of a new configuration inserts new data in the database
    '''

    connection_db, cursor = MyHandler.connect_to_DB()

    with connection_db:
        test_client.craft_POST('create test 1 2', verbose=False)
        test_client.craft_PUT('update test 2 3', verbose=False)

        cursor.execute('SELECT * FROM configuration WHERE id=%s', ('test',))
        res = cursor.fetchall()
        assert res[0][1] == '2'
        assert res[0][2] == '3'
        test_client.craft_DELETE('delete test', verbose=False)


def update_not_existing_config(test_client):
    '''
    Test if the update of a not existing configuration does not insert new data in the database
    '''

    connection_db, cursor = MyHandler.connect_to_DB()

    with connection_db:
        test_client.craft_PUT('update not_existing 2 3', verbose=False)
        cursor.execute('SELECT * FROM configuration WHERE id=%s', ('not_existing',))
        res = cursor.fetchall()
        assert len(res) == 0


if __name__ == '__main__':
    server_address = ('', PORT)
    httpd = MyServer(server_address, MyHandler)
    print('Starting configuration service on port %d...' % PORT)
    print('Testing...')
    thread_server = threading.Thread(target=httpd.run)
    thread_server.start()

    client = Client()

    create_new_config(client)
    create_existing_config(client)
    delete_existing_config(client)
    update_existing_config(client)
    update_not_existing_config(client)

    print('Test successfully completed!')
