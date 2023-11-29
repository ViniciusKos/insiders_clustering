FROM python:3.10.4
COPY . /app
WORKDIR /app
RUN apt update -y && apt install awscli -y
RUN pip install -r requirements.txt

CMD ["python3","app.py"]