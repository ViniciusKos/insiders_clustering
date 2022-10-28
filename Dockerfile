FROM ubuntu:latest

COPY req_simple.txt /opt/app/req_simple.txt
WORKDIR /opt/app
RUN apt update
RUN apt install python3 -y
RUN set apt-get install python3
RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r req_simple.txt
ENV AWS_ACCESS_KEY_ID=AKIAT5ISLT2BI5FYDZAX
ENV AWS_DEFAULT_REGION=sa-east-1
ENV AWS_SECRET_ACCESS_KEY=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


COPY . /opt/app