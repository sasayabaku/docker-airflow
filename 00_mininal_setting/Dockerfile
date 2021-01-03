FROM python:3.7-slim-buster

SHELL ["/bin/bash", "-l", "-c"]

# Airflow
ARG AIRFLOW_VERSION=2.0.0
ARG AIRFLOW_USER=airflow
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# ENV AIRFLOW_DB_CONN=sqlite:////usr/local/airflow/db/airflow.db

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

RUN mkdir -p ${AIRFLOW_HOME}
WORKDIR ${AIRFLOW_HOME}

# User Add & Super User setting & apt library install
RUN useradd -ms /bin/bash -d ${AIRFLOW_HOME} -G sudo ${AIRFLOW_USER} && \
    apt-get install -y --fix-broken && \
    apt-get autoremove && \
    apt-get update && apt-get -y upgrade && \ 
    apt-get install -y --no-install-recommends apt-utils \
    mariadb-client default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    build-essential \
    net-tools iputils-ping

# Python Library Install
RUN pip install --upgrade pip && pip install apache-airflow psycopg2 mysqlclient

# COPY local airflow directory
ADD ./airflow ${AIRFLOW_HOME}
COPY ./script/entrypoint.sh /entrypoint.sh

RUN chown -R ${AIRFLOW_USER}:${AIRFLOW_USER} ${AIRFLOW_USER_HOME}
RUN chmod +x /entrypoint.sh

EXPOSE 8080 5555 8793

USER ${AIRFLOW_USER}
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]