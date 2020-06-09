FROM python

COPY . /code

RUN cd /code && python setup.py install && cxaccess init && cxaccess version