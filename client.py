import json
import requests
import re
from utils import *

class Client():

    def craft_POST(self, user_input):
        user_input = user_input.split(' ')
        config_id, name, value = user_input[1], user_input[2], user_input[3]
        print('Performing POST request with id: {}, name: {}, value: {}'.format(config_id, name, value))
        new_config = {'id': config_id, 'name': name, 'value': value}
        new_config = json.dumps(new_config)
        response = requests.post('http://localhost:{}'.format(PORT), json=new_config)
        print((response.__getattribute__('content')).decode('utf-8'))

    def craft_GET(self, user_input):
        user_input = user_input.split(' ')
        config_id = user_input[1]
        print('Performing GET request with id: {}'.format(config_id))
        response = requests.get('http://localhost:{}'.format(PORT), params=config_id)
        if response.headers['content-type'] == 'application/json':
            content = response._content.decode('utf-8').replace("'", '"')
            content = json.loads(content)
            content = json.dumps(content, indent=4, sort_keys=True)
        else:
            content = (response.__getattribute__('content')).decode('utf-8')
        print(content)

    def craft_PUT(self, user_input):
        user_input = user_input.split(' ')
        config_id, name, value = user_input[1], user_input[2], user_input[3]
        print('Performing PUT request with id: {}, name: {}, value: {}'.format(config_id, name, value))
        new_config = {'id': config_id, 'name': name, 'value': value}
        new_config = json.dumps(new_config)
        response = requests.put('http://localhost:{}'.format(PORT), json=new_config)
        print((response.__getattribute__('content')).decode('utf-8'))

    def craft_DELETE(self, user_input):
        user_input = user_input.split(' ')
        config_id = user_input[1]
        print('Performing DELETE request with id: {}'.format(config_id))
        response = requests.delete('http://localhost:{}'.format(PORT), params=config_id)
        print((response.__getattribute__('content')).decode('utf-8'))

    def parse(self, user_input):
        if re.match(CREATE_REGEX, user_input):
            self.craft_POST(user_input)
        elif re.match(READ_REGEX, user_input):
            self.craft_GET(user_input)
        elif re.match(DELETE_REGEX, user_input):
            self.craft_DELETE(user_input)
        elif re.match(UPDATE_REGEX, user_input):
            self.craft_PUT(user_input)
        elif re.match(HELP, user_input):
            return self.run()
        else:
            print('Invalid output... please try again!')
        return self.read_input()


    def read_input(self):
        while True:
            user_input = input('What do you want to do?\n')
            self.parse(user_input)

    def run(self):
        print('Here is what you can do: \n \n'
              'Create a new config: create {ID} {NAME} {VALUE}\n'
              'Read an existing config: read {ID}\n'
              'Delete an existing config: delete {ID}\n'
              'Update an existing config: update {ID}\n \n' 
              'IDs can only be composed of digits\n'
              'Names, values can only be composed of lower-case letters\n \n'
              'Type \'help\' in any moment to read again the list of commands\n \n')
        self.read_input()

if __name__ == '__main__':
    client = Client()
    print('Hello! Welcome to Alessandro Paticchio\'s coding test for Buildo!\n')
    client.run()

