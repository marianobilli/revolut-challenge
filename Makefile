build:
	docker build . -t revolut-api:latest

libs: 
	# Uncomment the bellow two lines if you want to use venv
	# python3 -m venv venv
	# source venv/bin/activate
	python3 -m pip install -r app/requirements.txt
	python3 -m pip install -r integration-tests/requirements.txt

unit-tests: libs
	pytest app/unit_tests.py

integration-tests: libs build
	pytest integration-tests/tests.py --docker-compose integration-tests/docker-compose.yaml

tests: unit-tests integration-tests

run: build
	docker-compose -f integration-tests/docker-compose.yaml up -d
	@echo "\nNow you can call the api with curl. i.e:"
	@echo "\tcurl --insecure https://localhost:9000/hello/status   --request GET"
	@echo "\tcurl --insecure https://localhost:9000/hello/usertest --request PUT --header 'Content-Type: application/json' --data '{\"dateOfBirth\": \"2000-01-01\"}' -v"
	@echo "\tcurl --insecure https://localhost:9000/hello/usertest --request GET"

run-standalone-db:
	@echo "This is useful when running flask locally"	
	docker-compose -f standalone-db/docker-compose.yaml up -d

clean:
	@echo "Cleaning containers..."
	docker-compose -f integration-tests/docker-compose.yaml down 
	docker-compose -f standalone-db/docker-compose.yaml down 
