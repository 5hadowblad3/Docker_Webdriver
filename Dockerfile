FROM ubuntu
FROM python:2.7.13

MAINTAINER Shadow

RUN apt-get update && \
apt-get install -yf unzip libnss3-dev libxi6 libgconf-2-4 \
libxss1 libappindicator1 libindicator7

RUN pip install selenium
RUN wget https://chromedriver.storage.googleapis.com/2.9/chromedriver_linux64.zip && \
unzip chromedriver_linux64.zip && rm -rf chromedriver_linux64.zip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
dpkg -i google-chrome*.deb && rm -rf google-chrome*.deb
COPY chrome_case1.py .
COPY ecap.crx .
COPY food_case2.txt .

RUN ls

RUN python chrome_case1.py






