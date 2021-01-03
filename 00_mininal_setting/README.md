# Minimal Setting

## Goal
[AirflowのQuick Start](https://airflow.apache.org/docs/apache-airflow/stable/start.html)を実行して、サンプルプログラムを実行する。

![](./docs/arch-diag-basic.png)
Reffer from [Quick Start — Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/start.html#basic-airflow-architecture)


## Airflow 設定変更

Metadata DBを別のDockerコンテナで運用するため、
`airflow.cfg`内の設定を変更。

**L.30**
```ApacheConf
Format) sql_alchemy_conn = postgresql://[DBのユーザ名]:[DBのパスワード]@[DBのPATH]:[DBのPort]/airflow
↓↓↓↓↓
This Sample) sql_alchemy_conn = postgresql://airflow:airflow@airflow_postgres:5432/airflow
```

**L.679**
```ApacheConf
Format) result_backend = postgresql://[DBのユーザ名]:[DBのパスワード]@[DBのPATH]:[DBのPort]/airflow
↓↓↓↓↓
This Sample) result_backend = postgresql://airflow:airflow@airflow_postgres:5432/airflow
```

## 初回設定

### PostgreDBの設定

本サンプルは、PostgreDBで、AirflowのMetadata DBを構築。  
Docker volumeの名前付きボリュームで永続化を設定。

`docker-compose.yml`

#### Volume設定

固定のVolumeを作成するように、`name`を指定

```yaml
volumes:
  airflow_db:
    name: airflow_db
```


#### コンテナ設定

DBコンテナ(postgres)を設定。

```yaml
services:
  postgres:
    image: postgres:9.6
    environment:
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
      - POSTGRES_DB=airflow

    container_name: airflow_postgres

    volumes:
      - airflow_db:/var/lib/postgresql/data

```

## Web Server と Schedulerを起動
```bash
$ docker-compose up -d --build
```

しかし、この状態では、Airflowユーザが作れられていないので起動に失敗します。

### Airflowユーザの作成
Bashでログイン。
```bash
docker run -it --rm --net=airflow_network my_airflow_webserver bash
```

以下コンテナ内

```bash
$ airflow db init

$ airflow users create \
    --username airflow \
    --firstname Apache \
    --lastname Airflow \
    --role Admin \
    --email a.apache@airflow.example

この後、パスワードを要求されます。
```

## Web Serverにログイン

webserverとschedularに、
```yaml
restart: always
```
を設定しているため、正常稼働するまで再起動するので、

http://localhost:8080
でWeb Serverにログインできるようになる。