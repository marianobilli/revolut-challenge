# revolut-challenge

## Prerequisites
`Python3` and `Docker` have to be installed
<p></p> &nbsp;

## Local execution
Setup, testing, runing and cleaning up is all encapsulated in the make file
```
# To run all tests
$ make tests

# To start the service locally (the output will give some curl examples on how to call the service)
$ make run

# If you want to run the app locally ensure to have running db 
$ make run-standalone-db

# To stop and cleanup all containers
$ make clean
```