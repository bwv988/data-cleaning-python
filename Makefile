# Makefile for running the project containers.

setup:
	# Create a persistent volume for the DB.
	docker volume create --name pgdata
	
clean:
	docker volume rm pgdata

