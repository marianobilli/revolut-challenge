# Integration Tests

## 1. build the api container
```
/ $ docker build . -t revolut-api:latest # image name is important as it is user in docker-compose.yaml
```

## 2. Install pip requirements
```
integration-tests/ $ python3 -m pip install -r requirements.txt
```

## 3. Execute tests
```
integration-tests/ $ pytest tests.py --docker-compose docker-compose.yaml -v
```