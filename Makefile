NAME=thefab/autoclean-vsftpd
VERSION=$(shell ./version.sh)

build:
	docker build -f Dockerfile -t $(NAME):$(VERSION) .

debug: build
	docker run -i -t -e AUTOCLEANFTP_PASV_ADDRESS=`hostname -i` -p 20:20 -p 21:21 -p 21100-21110:21100-21110 $(NAME):$(VERSION) bash

release:
	if test "$(VERSION)" != "dev" -a "${DOCKER_PASSWORD}" != ""; then docker login -e="${DOCKER_EMAIL}" -u="${DOCKER_USERNAME}" -p="${DOCKER_PASSWORD}"; docker push $(NAME):$(VERSION); fi
