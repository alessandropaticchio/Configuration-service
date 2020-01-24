# Coding Test Buildo
This repository contains my Coding Test for Buildo. It is a Python 3.7 implementation of a configuration service, accessible via
HTTP API, that stores configurations and allows to create, read, update and delete them.
Configurations have the form:

```
{

    "id": "some-id",
    "name": "Configuration for Foo",
    "value": "This is the value for configuration Foo"
    
}
```

## Architecture
The architecture is a basic 3-tier, with Client, Server and Database.

* The client is a simple Command Line Interface, that parses the input of the user and craft HTTP requests accordingly.
  I decided to implement this client to make the interaction easier.
* The server is a web server, developed by using the Python built-in support HTTPServer. 
* The database is a relational database, hosted by the PaaS Heroku, with only one table with the following structure:

```
TABLE: CONFIGURATION
{
    ID VARCHAR PRIMARYKEY
    NAME VARCHAR
    VALUE VARCHAR
}
```

The chosen DBMS is PostgreSQL, which is Open Source and allows a better manipulation for JSON Objects.

## Getting started
Before starting, it is necessary to create a new Virtual Environment and install all the dependencies of the project.

```
pip install -r requirements.txt
```

### How to run

Once all the dependencies are installed, just activate your Python Virtual Environment, go in the directory of the project
and launch the server.

```
python server.py
```

The server will listen for requests at:

```
http://localhost:8080/
```

### How to use the client

To launch the client:

```
python client.py
```

A set of instructions for querying the service will be listed, here are some examples of interaction to create,
read, update and delete configurations:

```
create ID NAME VALUE
read ID
delete ID
update ID NAME VALUE
```

* The "create" operation will craft a POST request, with a JSON Object in the body
* The "read" operation will craft a GET request, with the ID in the request's parameters
* The "delete" operation will craft a DELETE request, , with the ID in the request's parameters
* The "update" operation will craft an UPDATE request, with a JSON Object in the body

The server will reply with JSON objects containing the response, if the request is consistent.
Otherwise an error is signaled.

### How to make requests outside the client

Of course the server is accessible even outside the client.

In order to make GET/DELETE requests for an ID, it will listen at:

```
http://localhost:8080/?ID
```

In order to make POST/PUT requests, it will listen at:

```
http://localhost:8080/
```

with a JSON Object in the body:

```
{

    "id": "some-id",
    "name": "Configuration for Foo",
    "value": "This is the value for configuration Foo"
    
}
```

### Tests

Due to the tiny structure of the architecture and to the fact that the server only does operations when the
client asks for it, I used an integration approach that makes me sure that:

* The requests sent by the client get consistent responses
* The requests received by the server trigger the right manipulation of the database

The tests documentation is provided in the files:

```
client_to_server_tests.py
server_from_client_tests.py
```

### How to contribute
