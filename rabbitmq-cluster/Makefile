SHELL := /bin/bash

.PHONY: all
all: greet

project-name=rmq-cluster

up:
	@echo Start ${project-name} Service: && \
	docker stack deploy --detach=false -c docker-compose.yml ${project-name}
down:
	@echo Shut down ${project-name} Service: && \
	docker stack rm ${project-name}
