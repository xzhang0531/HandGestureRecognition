FROM ubuntu:latest


RUN apt-get update
RUN apt-get install -y python3-pip python3-dev


RUN pip3 install --upgrade pip
RUN rm -r /root/.cache

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade tensorflow

ENTRYPOINT ["python3"]
CMD ["server.py"]

