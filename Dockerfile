FROM ubuntu:18.04

RUN apt update
RUN apt upgrade -y
RUN apt install -y python3-pip
ADD src /proxy/
WORKDIR /proxy/
EXPOSE 5000
ENTRYPOINT ["sh", "./start.sh"]
