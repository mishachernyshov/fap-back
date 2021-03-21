FROM python:3.9.2
ENV PYTHONUNBUFFERED=1

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && pip3 install --upgrade pip \
    && apt-get install -yqq \
        build-essential \
        python3-dev \
        apt-utils \
        binutils \
        libproj-dev \
        gdal-bin \
        git \
    && apt-get autoclean -yqq \
    && apt-get autoremove -yqq

RUN apt-get update && apt-get install -yqq wget lsb-release
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update && apt-get install -yqq postgresql-client-13
RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.1.2/mkcert-v1.1.2-linux-amd64
RUN mv mkcert-v1.1.2-linux-amd64 mkcert
RUN chmod +x mkcert
RUN cp mkcert /usr/local/bin/
RUN mkcert -install

WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/