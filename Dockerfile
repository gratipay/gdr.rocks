FROM ubuntu:latest
RUN apt-get -y update && apt-get install -y python python-pip git && apt-get build-dep -y lxml
RUN pip install --upgrade pip
RUN pip install virtualenv
COPY gdr.py ./
ENTRYPOINT ["./gdr.py"]
