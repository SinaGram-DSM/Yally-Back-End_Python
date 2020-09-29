FROM ubuntu:18.04
MAINTAINER tpwns072@gmail.com

RUN apt-get update -y
RUN apt-get install -y python3.7
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y libssl-dev
RUN apt-get install -y libmysqlclient-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["export", "PYTHONPATH='$PWD'"]

WORKDIR /app/server
CMD ["flask", "run", "--host=0.0.0.0"]
