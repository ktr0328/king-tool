# KCG Tool

学内サイトスクレイピング

スクレイピングというか King の API を叩いてる

DB は叩いた API のレスをそのまま入れてるから正規化もしてなくて汚い

エンドポイントを叩けば JSON でデータが返ってきます。

1 枚だけ画面があり。

![img](https://user-images.githubusercontent.com/25787913/53440270-7b770f00-3a47-11e9-8a70-4a199eb7ab7d.png)

ローカルはいい。速い。

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

1. run MySQL @{config.yml - uri}

   - ex.`docker run --rm -p 3306:3306 -e MYSQL_ROOT_PASSWORD=king -e MYSQL_DATABASE=king -d mysql`
   - overwrite `config.yml` -> `uri: "sqlite:///:memory:"`

2. `pip install -r requirements.txt`

3. `python main.py`

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
    host: "0.0.0.0"
    # host: '127.0.0.1'
    port: 5000
    debug: False
```
