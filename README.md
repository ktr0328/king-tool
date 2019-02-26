# KCG Tool

scraping from King-lms

スクレイピングというかAPI叩いてる

DBは叩いたAPIをそのまま入れてるから汚い

ついでだから画面も作っちゃった

## Setup

```sh
cp .envrc.template .envrc
```

fill environment variables

or

export each env

- USER_ID
- PASSWORD

## Usage

### Direct

1. run MySQL and create database {config.yml - uri}

2. pip install { below you need }

3. `python main.py`

pip

- flask
- flask_cors
- requests
- yaml

### On Docker

1. `docker-compose up -d`

default: [http://0.0.0.0:5000](http://0.0.0.0:5000)

## Configure

```yml
# config.yml
service:
  db:
    # mysql+pymysql://<user>:<password>@<host>/<database>?charset=utf8
    uri: "mysql+pymysql://root:king@127.0.0.1/king?charset=utf8"
    # uri: "sqlite:///:memory:" # Fast!
    encoding: utf-8
    echo: False
  server:
    host: '0.0.0.0'
    # host: '127.0.0.1'
    port: 5000
    debug: False
```
