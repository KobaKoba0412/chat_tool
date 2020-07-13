# 公式からpython3.7 on alpine linuxイメージをpull
FROM python:3.7-alpine

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 環境変数を設定
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1

#各種コマンドインストール(gcc,openssl-dev必須)
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && apk add postgresql-dev \
    && apk add --no-cache curl \
    && apk add build-base libffi-dev \
    && apk del build-deps\
    && apk add openssl-dev

# Pipenvをインストール
RUN pip install --upgrade pip \
    && pip install pipenv \
    && pip install psycopg2

# ホストのpipfileをコンテナの作業ディレクトリにコピー
COPY ./Pipfile /usr/src/app/Pipfile

# pipfileからパッケージをインストールしてDjango環境を構築
RUN pipenv install --skip-lock --system --dev

# entrypoint.shをコピー
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# ホストのカレントディレクトリ（現在はappディレクトリ）を作業ディレクトリにコピー
COPY . /usr/src/app/

# entrypoint.shを実行
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]