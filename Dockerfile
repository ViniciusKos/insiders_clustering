FROM ubuntu:latest

COPY req_simple.txt /opt/app/req_simple.txt
WORKDIR /opt/app
RUN apt update
RUN apt install python3 -y
RUN set apt-get install python3
RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r req_simple.txt



COPY . /opt/app