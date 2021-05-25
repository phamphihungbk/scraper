.PHONY: up ## docker up
up:
	docker-compose -f ./environment/docker-compose.yml up -d --remove-orphans

.PHONY: build ## docker build
build:
	docker-compose -f ./environment/docker-compose.yml build

.PHONY: docker-down ## docker stop
down:
	docker-compose -f ./environment/docker-compose.yml down --remove-orphans

.PHONY: pip-install ## install dependencies with pip
pip-install:
	docker exec -it scrapper-python sh -c "pip install -r requirements.txt"

.PHONY: check-verison ## check version of dependencies
check-version:
	docker exec -it scrapper-python sh -c "geckodriver --version"
