FROM ubuntu:18.04

RUN apt update \
 && DEBIAN_FRONTEND=noninteractive  apt upgrade -y \
 && DEBIAN_FRONTEND=noninteractive apt -y install \
 		dialog debhelper \
		dh-python intltool python3-all python3-setuptools devscripts
