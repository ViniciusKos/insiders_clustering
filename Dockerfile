FROM ubuntu:latest

WORKDIR /opt/app
RUN apt update
RUN apt install python3.10 -y
RUN apt-get update && apt-get install -y python3-pip 
RUN apt install sudo
RUN apt install -y git
RUN sudo apt-get install libpq-dev python3 -y

##COPY . /opt/app

RUN pip install -r req_simple.txt


CMD [ "python3", "./run_deploy.py" ]