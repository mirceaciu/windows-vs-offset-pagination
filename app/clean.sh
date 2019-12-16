#!/bin/bash

docker-compose down
docker rm -f $(docker ps -a -q)
#docker rmi -f $(docker images | grep "windowvsoffset")
docker rmi -f $(docker images | grep "<none")
yes | docker volume prune
docker-compose build
docker-compose up
