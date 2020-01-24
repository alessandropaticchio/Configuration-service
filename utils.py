PORT = 8080

WELCOME_MESSAGE = 'Hello! This is Alessandro Paticchio\'s coding test for Buildo!\n'

COMMAND_MESSAGE = ('Here is what you can do: \n \n'
                  'Create a new config: create {ID} {NAME} {VALUE}\n'
                  'Read an existing config: read {ID}\n'
                  'Delete an existing config: delete {ID}\n'
                  'Update an existing config: update {ID} {NAME} {VALUE}\n \n'
                  'IDs, names, values can be composed by lower-case/upper-case letters and/or digits\n \n'
                  'Type \'help\' in any moment to read again the list of commands')

CREATE_REGEX = r'create [a-zA-Z0-9]+ [a-zA-Z0-9]+ [a-zA-Z0-9]+$'
UPDATE_REGEX = r'update [a-zA-Z0-9]+ [a-zA-Z0-9]+ [a-zA-Z0-9]+$'
DELETE_REGEX = r'delete [a-zA-Z0-9]+$'
READ_REGEX = r'read [a-zA-Z0-9]+$'
HELP = r'help$'

NO_SUCH_ID_ERROR = "There is no configuration with the config id provided\n"
OPERATION_SUCCESSFUL = 'Success!\n'
ALREADY_ID_ERROR = "There is already a configuration with the provided config id\n"
SERVER_NOT_AVAILABLE = 'Server not yet available...\n'
INVALID_INPUT = 'Invalid input... please try again!\n'

DATABASE_URL = 'postgres://iuseeinjexykof:522f12d7a2090fc3e7140100272200837c8748bd8ea869ae68288893b7' \
               'e75aa6@ec2-54-247-82-14.eu-west-1.compute.amazonaws.com:5432/d8vfb8b2ige41o'
dbname = 'd8vfb8b2ige41o'
user = 'iuseeinjexykof'
password = '522f12d7a2090fc3e7140100272200837c8748bd8ea869ae68288893b7e75aa6'
host = 'ec2-54-247-82-14.eu-west-1.compute.amazonaws.com'
port = 5432

LOCK_ID = 123