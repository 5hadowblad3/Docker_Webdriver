FROM markadams/chromium-xvfb-py2

MAINTAINER Shadow


COPY chrome_case1.py .
COPY ecap.crx .
COPY food_case2.txt .
#COPY test.py .

#RUN python test.py 

RUN python chrome_case1.py






