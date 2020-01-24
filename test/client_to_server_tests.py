from client import Client
from server import *
import threading

'''This file is used to test the integration between client and server. It tests that all the requests sent from
the client to the server are consistent with the expected outcomes.'''


def create_new_config(test_client):
    '''
    Test if the creation of a new configuration is successful
    '''
    response = test_client.craft_POST('create test 1 2', verbose=False)
    assert response.status_code == 200
    assert response.text == OPERATION_SUCCESSFUL
    test_client.craft_DELETE('delete test', verbose=False)


def create_existing_config(test_client):
    '''
    Test if the creation of an already existing configuration fails
    '''
    test_client.craft_POST('create test 1 2', verbose=False)
    response = test_client.craft_POST('create test 1 2', verbose=False)
    assert response.status_code == 400
    assert response.text == ALREADY_ID_ERROR
    test_client.craft_DELETE('delete test', verbose=False)


def delete_existing_config(test_client):
    '''
    Test if the deletion of an existing configuration is successful
    '''
    test_client.craft_POST('create test 1 2', verbose=False)
    response = test_client.craft_DELETE('delete test', verbose=False)
    assert response.status_code == 200
    assert response.text == OPERATION_SUCCESSFUL


def delete_not_existing_config(test_client):
    '''
    Test if the deletion of a not existing configuration fails
    '''
    response = test_client.craft_DELETE('delete not_existing', verbose=False)
    assert response.status_code == 400
    assert response.text == NO_SUCH_ID_ERROR


def update_existing_config(test_client):
    '''
    Test if the update of an existing configuration is successful
    '''
    test_client.craft_POST('create test 1 2', verbose=False)
    response = test_client.craft_PUT('update test 10 20', verbose=False)
    assert response.status_code == 200
    assert response.text == OPERATION_SUCCESSFUL
    test_client.craft_DELETE('delete test', verbose=False)


def update_not_existing_config(test_client):
    '''
    Test if the update of a not existing configuration fails
    '''
    response = test_client.craft_PUT('update not_existing 10 20', verbose=False)
    assert response.status_code == 400
    assert response.text == NO_SUCH_ID_ERROR


def read_existing_config(test_client):
    '''
    Test if the reading of an existing client is successful
    '''
    test_client.craft_POST('create test 1 2', verbose=False)
    response = test_client.craft_GET('read test', verbose=False)
    assert response.status_code == 200
    test_client.craft_DELETE('delete test', verbose=False)


def read_not_existing_config(test_client):
    '''
    Test if the update of an existing configuration fails
    '''
    response = test_client.craft_GET('read not_existing', verbose=False)
    assert response.status_code == 400
    assert response.text == NO_SUCH_ID_ERROR


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
    delete_not_existing_config(client)
    update_existing_config(client)
    update_not_existing_config(client)
    read_existing_config(client)
    read_not_existing_config(client)

    print('Test successfully completed!')