FROM ubuntu
FROM python:2.7.13

MAINTAINER Shadow


RUN add-apt-repository "deb http://dl.google.com/linux/chrome/deb/ stable main" && \
apt-get update && apt-get install -yf unzip libnss3-dev libxi6 libgconf-2-4 google-chrome-stable

RUN pip install selenium
RUN wget https://chromedriver.storage.googleapis.com/2.9/chromedriver_linux64.zip && \
unzip chromedriver_linux64.zip && rm -rf chromedriver_linux64.zip

COPY chrome_case1.py .
COPY ecap.crx .
COPY food_case2.txt .

RUN ls

RUN python chrome_case1.py






