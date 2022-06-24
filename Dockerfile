FROM python:latest

MAINTAINER andrii@qa.com

RUN apt-get update && apt-get -y install vim

RUN mkdir /automation

COPY ./src /automation/PythonTests/src
COPY ./tests /automation/PythonTests/tests
COPY ./utilities /automation/PythonTests/utilities

COPY ./setup.py /automation/PythonTests/
COPY ./pytest.ini /automation/PythonTests/
COPY ./env.sh /automation/PythonTests/
RUN mkdir /automation/PythonTests/logs

ADD ./requirements.txt /automation/PythonTests
WORKDIR /automation/PythonTests
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python setup.py install