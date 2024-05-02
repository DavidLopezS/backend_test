DOCKER_NAME=linkedin_backend_test

CURRENT_DIR=$(patsubst %/,%,$(dir $(realpath $(firstword $(MAKEFILE_LIST)))))
ROOT_DIR=$(CURRENT_DIR)
DOCKER_COMPOSE?=docker-compose
DOCKER_COMPOSE_RUN=$(DOCKER_COMPOSE) run --rm

# Detect the operating system
ifeq ($(OS),Windows_NT)
    CURRENT_USER=
    DOCKER_EXEC_TOOLS_APP=docker exec -it $(DOCKER_NAME) sh
else
    CURRENT_USER=sudo
    DOCKER_EXEC_TOOLS_APP=$(CURRENT_USER) docker exec -it $(DOCKER_NAME) sh
endif

PYTHON_INSTALL="pip install -r requirements.txt"

#
# Exec containers
#
.PHONY: app

app:
	$(DOCKER_EXEC_TOOLS_APP)

#
# Helpers
#
.PHONY: fix-permission

fix-permission:
	$(CURRENT_USER) chown -R ${USER}: $(ROOT_DIR)/

#
# Commands
#
.PHONY: build install up start first stop restart clear

build:
	$(DOCKER_COMPOSE) up --build -d

install:
	$(DOCKER_EXEC_TOOLS_APP) -c $(PYTHON_INSTALL)

up:
	$(DOCKER_COMPOSE) up 
	# TODO: Descomentar la parte de abajo si se quiere ejecutar en segundo plano
	# $(DOCKER_COMPOSE) up -d

start: up

first: build install up

stop: $(ROOT_DIR)/docker-compose.yml
	$(DOCKER_COMPOSE) down

restart: stop start

clear: stop $(ROOT_DIR)/docker-compose.yml
	$(DOCKER_COMPOSE) down -v --remove-orphans