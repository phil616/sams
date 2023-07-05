
  #    Dockerfile
  #    ~~~~~~~~~
  #    Dockerfile的docker部署，暴露80端口，使用清华源
  #    :copyright: (c) 2023 by Fei Dongxu.
  #    :date: 2023.07.04
  #    :license: Apache Licence 2.0
  #    Open mapping directories:
  #    1. /app/logs
  #    2. /app/storage

FROM python:3.9
WORKDIR /app

COPY . /app

ENV DB_HOST localhost
ENV DB_PORT 3306
ENV DB_NAME sams
ENV DB_USER root
ENV DB_PASSWORD 123456

ENV CACHE_HOST localhost
ENV CACHE_PORT 6379

ENV APP_INIT_SECRET abcdefg

ENV JWT_SECRET_KEY abcdefghijklmnopqrstuvwxyz

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "80"]
