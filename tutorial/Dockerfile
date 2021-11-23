FROM python:3.8
#LABEL maintainer twtrubiks
ENV PYTHONUNBUFFERED 1
RUN mkdir /tutorial
WORKDIR /tutorial
RUN apt-get update && apt-get install -y libaio1 wget unzip \
&& wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
&& unzip instantclient-basiclite-linuxx64.zip \
&& rm -f instantclient-basiclite-linuxx64.zip \
&& cd /tutorial/instantclient* \
&& rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci \
&& echo /tutorial/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
&& ldconfig
COPY . /tutorial/
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "/tutorial/manage.py", "runserver", "0.0.0.0:80"]
