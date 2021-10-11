# revolut-challenge

## **Test endpoint**
```
curl https://revolut-challenge.marianobilli.link/hello/usertest
```

## **Infrastructure View**
All infrastructure is created with terraform.
- VPC, Subnets, Route Tables, Internet gateway, segurity groups
- IAM roles and policies
- Kubernetes Cluster
- RDS (Database)
- FluxCD Manifests (https://fluxcd.io/)

<p align="left">
  <img src="documentation/images/infrastructure.png" width="750" title="Infrastructure Diagram">
</p>

## **Kubernetes View**
All configuration is applied via FluxCD which pulls all kubernetes manifests from this github repo and applies all found in kubernetes/ folder.
- external-dns ( to manage dns configuration )
- aws-application-load-balancer-controler ( to manage alb )
- cluster-autoscaler ( to manage autoscaling groups for scale-out/in based on cluster load )
- metric-server ( for measuring cluster load )
- revolut-challenge application 

<p align="left">
  <img src="documentation/images/kubernetes.png" width="950" title="Infrastructure Diagram">
</p>

## **Application View**
The application is written in python and uses the following libraries
- Flask
- SQLAlchemy
- Pytest

<p align="left">
  <img src="documentation/images/application.png" width="550" title="Infrastructure Diagram">
</p>


## Local execution / Unit and Integration Tests
Setup, testing, runing and cleaning up is all encapsulated in the make file. `Python3` and `Docker` have to be installed
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