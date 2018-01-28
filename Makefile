# Makefile for the project.

setup:
	# Create a persistent volume for the DB.
	docker volume create --name pgdata
	
clean:
	docker volume rm pgdata

