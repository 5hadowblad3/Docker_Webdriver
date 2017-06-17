FROM ubuntu:14.04
FROM python:2.7.13

MAINTAINER Shadow


RUN pip install selenium

RUN wget https://chromedriver.storage.googleapis.com/2.30/chromedriver_linux64.zip && \
tar zxvf chromedriver_linux64.zip \ rm -rf chromedriver_linux64.zip

COPY chrome_case1.py .
COPY food_case2.txt .

RUN python chrome_case1.py






