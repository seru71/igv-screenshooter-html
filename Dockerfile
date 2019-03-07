FROM ubuntu:18.04

LABEL authors="Pawel Sztromwasser"

WORKDIR /igv-screenshooter-html

COPY ./ /igv-screenshooter-html

RUN apt update \
 && apt install -y locales python3 python3-pip virtualenv \
 && locale-gen "en_US.UTF-8" \
 && virtualenv -p python3 .venv \
 && pip3 install -r requirements.txt \
 && ln -s /igv-screenshooter-html/shoot.py /usr/local/bin \
 && chmod u+x /igv-screenshooter-html/shoot.py
  
ENV LANG en_US.UTF-8  

 
    
