FROM python

COPY . /code

RUN cd /code && ls -la && python setup.py install && cxaccess init && cxaccess version