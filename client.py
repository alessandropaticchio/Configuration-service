import json
import requests
import re
from utils import *
import socket


class Client():

    '''
    This class is the client class and it is used to do GET/POST/PUT/DELETE requests to the server. It parses input
    from the user and craft a new request accordingly.
    '''

    def craft_POST(self, user_input, verbose=True):
        '''
        :param user_input: a string like 'create id name value', which is then unpacked in a json and sent to the server
        :param verbose: if True, it prints the output of the operation
        :return: response, a Response object that contains the answer from the server
        '''
        user_input = user_input.split(' ')
        config_id, name, value = user_input[1], user_input[2], user_input[3]
        if verbose:
            print('Performing POST request with id: {}, name: {}, value: {}\n'.format(config_id, name, value))
        try:
            new_config = {'id': config_id, 'name': name, 'value': value}
            new_config = json.dumps(new_config)
            response = requests.post('http://localhost:{}'.format(PORT), json=new_config)
            if verbose:
                print((response.__getattribute__('content')).decode('utf-8'))
            return response
        except socket.error:
            print(SERVER_NOT_AVAILABLE)

    def craft_GET(self, user_input, verbose=True):
        '''
        :param user_input: a string like 'read id', which is then unpacked and sent with the parameters
                           of the get request
        :param verbose: if True, it prints the output of the operation
        :return: response, a Response object that contains the answer from the server
        '''
        user_input = user_input.split(' ')
        config_id = user_input[1]
        if verbose:
            print('Performing GET request with id: {}\n'.format(config_id))
        response = requests.get('http://localhost:{}'.format(PORT), params=config_id)
        try:
            if response.headers['content-type'] == 'application/json':
                content = response._content.decode('utf-8').replace("'", '"')
                content = json.loads(content)
                content = json.dumps(content, indent=4, sort_keys=True)
            else:
                content = (response.__getattribute__('content')).decode('utf-8')
            if verbose:
                print(content)
            return response
        except socket.error:
            print(SERVER_NOT_AVAILABLE)

    def craft_PUT(self, user_input, verbose=True):
        '''
        :param user_input: a string like 'update id name value', which is then unpacked in a json and sent to the server
        :param verbose: if True, it prints the output of the operation
        :return: response, a Response object that contains the answer from the server
        '''
        user_input = user_input.split(' ')
        config_id, name, value = user_input[1], user_input[2], user_input[3]
        if verbose:
            print('Performing PUT request with id: {}, name: {}, value: {}\n'.format(config_id, name, value))
        try:
            new_config = {'id': config_id, 'name': name, 'value': value}
            new_config = json.dumps(new_config)
            response = requests.put('http://localhost:{}'.format(PORT), json=new_config)
            if verbose:
                print((response.__getattribute__('content')).decode('utf-8'))
            return response
        except socket.error:
            print(SERVER_NOT_AVAILABLE)

    def craft_DELETE(self, user_input, verbose=True):
        '''
        :param user_input: a string like 'delete id', which is then unpacked and sent with the parameters
                           of the get request
        :param verbose: if True, it prints the output of the operation
        :return: response, a Response object that contains the answer from the server
        '''
        user_input = user_input.split(' ')
        config_id = user_input[1]
        if verbose:
            print('Performing DELETE request with id: {}'.format(config_id))
        try:
            response = requests.delete('http://localhost:{}'.format(PORT), params=config_id)
            if verbose:
                print((response.__getattribute__('content')).decode('utf-8'))
            return response
        except socket.error:
            print(SERVER_NOT_AVAILABLE)

    def parse(self, user_input):
        '''
        This function parses the input of the user and, if correctly parsed, sends a request to the server.
        :param user_input: a string like:
                           create id name value,
                           read id,
                           update id name value,
                           delete id
        '''
        if re.match(CREATE_REGEX, user_input):
            self.craft_POST(user_input)
        elif re.match(READ_REGEX, user_input):
            self.craft_GET(user_input)
        elif re.match(DELETE_REGEX, user_input):
            self.craft_DELETE(user_input)
        elif re.match(UPDATE_REGEX, user_input):
            self.craft_PUT(user_input)
        elif re.match(HELP, user_input):
            return self.start()
        else:
            print(INVALID_INPUT)
        return self.read_input()


    def read_input(self):
        while True:
            user_input = input('What do you want to do?\n')
            self.parse(user_input)

    def start(self):
        print(COMMAND_MESSAGE)
        self.read_input()


if __name__ == '__main__':
    print(WELCOME_MESSAGE)
    client = Client()
    client.start()
