FROM python:3.10.4
RUN apt update -y
COPY requirements_prod.txt .
RUN pip install -r requirements_prod.txt
RUN apt install awscli -y
COPY . /app
WORKDIR /app

CMD ["python","app.py"]