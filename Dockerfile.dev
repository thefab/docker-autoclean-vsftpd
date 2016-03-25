FROM thefab/centos-opinionated:centos6
MAINTAINER Fabien MARTY <fabien.marty@gmail.com>

ENV AUTOCLEANFTP_SYSLOG=1 \
    AUTOCLEANFTP_LOCAL_UMASK=022 \
    AUTOCLEANFTP_USERS=demo1,demo2 \
    AUTOCLEANFTP_PASSWORDS=demo1,demo2 \
    AUTOCLEANFTP_UIDS=500,501 \
    AUTOCLEANFTP_GIDS=500,500 \
    AUTOCLEANFTP_LIFETIMES=60,60 \
    AUTOCLEANFTP_PASV_MIN_PORT=21100 \
    AUTOCLEANFTP_PASV_MAX_PORT=21110 \
    AUTOCLEANFTP_PASV_ADDRESS=FIXME

# Install vsftp and some dependencies
RUN yum -y install vsftpd util-linux-ng passwd && rm -f /etc/vsftpd/vsftpd.conf

# Add custom files
COPY root /

VOLUME ["/data"]
EXPOSE 21 21100-21110
