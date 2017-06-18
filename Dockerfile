FROM ubuntu:14.04
FROM python:2.7.13

MAINTAINER Shadow


RUN apt-get update && apt-get install -y unzip libnss3-dev libxi6 libgconf-2-4 chromium-browser

RUN pip install selenium
RUN wget https://chromedriver.storage.googleapis.com/2.9/chromedriver_linux64.zip && \
unzip chromedriver_linux64.zip && rm -rf chromedriver_linux64.zip

COPY chrome_case1.py .
COPY ecap.crx .
COPY food_case2.txt .

RUN ls

RUN python chrome_case1.py






