FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install python3-pip -y

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN pip3 install -r requirements.txt
WORKDIR /app/server

EXPOSE 5000 80

CMD ["flask", "run"]
