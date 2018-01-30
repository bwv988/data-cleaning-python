# Makefile for running the project containers.
all: clean

setup:
	docker volume create --name pgdata
	
clean:
	docker volume rm pgdata

