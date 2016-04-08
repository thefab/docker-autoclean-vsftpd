build:
	docker build -f Dockerfile -t thefab/autoclean-vsftpd:latest .

debug: build
	docker run -i -t -e AUTOCLEANFTP_PASV_ADDRESS=`hostname -i` -p 20:20 -p 21:21 -p 21100-21110:21100-21110 thefab/autoclean-vsftpd:latest bash
