NAME=thefab/autoclean-vsftpd
TAG=latest
VERSION=$(shell cat VERSION)


build:
	docker build -f Dockerfile -t $(NAME):$(TAG) .

debug: build
	docker run -i -t -e AUTOCLEANFTP_PASV_ADDRESS=`hostname -i` -p 20:20 -p 21:21 -p 21100-21110:21100-21110 $(NAME):$(TAG) bash

release: build
	docker login -e="${DOCKER_EMAIL}" -u="${DOCKER_USERNAME}" -p="${DOCKER_PASSWORD}"
	docker push thefab/autoclean-vsftpd
