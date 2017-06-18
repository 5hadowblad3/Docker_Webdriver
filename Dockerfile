FROM ubuntu:14.04
FROM python:2.7.13

MAINTAINER Shadow


RUN apt-get update && apt-get install -y unzip libnss3-dev
RUN pip install selenium==3.0.0b3
RUN wget https://chromedriver.storage.googleapis.com/2.9/chromedriver_linux64.zip && \
unzip chromedriver_linux64.zip && rm -rf chromedriver_linux64.zip

COPY chrome_case1.py .
COPY ecap.crx .
COPY food_case2.txt .

RUN python chrome_case1.py






