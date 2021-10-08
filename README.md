# revolut-challenge

## Prerequisites
`Python3` and `Docker` have to be installed
<p></p> &nbsp;

## Makefile
Setup, testing, runing and cleaning up is all encapsulated in the make file
```
# To run all tests
$ make tests

# To start the service locally (the output will give some curl examples on how to call the service)
$ make run

# To stop and cleanup all containers
$ make clean
```

## VSCODE
This example `launch.json` will allow to run flask locally in debug mode. ensure to run first `make run-standalone-db` in order to have local running database
```
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "./app/api.py",
                "FLASK_ENV": "development",
                "FLASK_RUN_PORT": "9000",
                "DB_USERNAME": "revolut",
                "DB_PASSWORD": "challenge",
                "DB_PORT": "5432",
                "DB_HOST": "localhost",
                "LOG_LEVEL": "INFO"
            },
            "args": [
                "run",
            ],
            "jinja": true
        }
    ]
}
```