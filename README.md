# Name（リポジトリ/プロジェクト/OSSなどの名前）
 
chat_tool

# Server configuration
▼デバッグ環境  
    アプリケーションサーバー   ⇒   Django付属の開発サーバー  
    DBサーバー                 ⇒   SQLite  
    Channel Layer　　          ⇒   redis  

▼本番環境  
    アプリケーションサーバー   ⇒   Gunicorn  
    DBサーバー                 ⇒   PostgreSQL  
    Channel Layer　　          ⇒   redis  
    リバースプロキシ           ⇒   Nginx  

# Usage
 Docker Composeを使用して、デバッグ環境または、本番環境の構築を行えるようにしています。  
 以下それぞれのymlファイルになります。  

    デバッグ環境　  ・・・ Docker_development.yml  
    本番環境　      ・・・ Docker_production.yml  

デバッグ環境なら、  

    docker-compose -f Docker_development.yml up --build  

本番環境なら、  

    docker-compose -f Docker_production.yml up --build  

のコマンドによって環境の構築を行うことが出来ます。  

コンテナの停止/削除を行いたい場合は以下のコマンドを実行します。（デバッグ環境のみ記載）  

    docker-compose -f Docker_development.yml down -v  

▼接続先のIPについて  
"docker-machine ip"により確認できます。  
また、PORTはデバッグ環境では8000、本番環境では1337が解放されています。  
 
# Note
本番環境での注意点があります。  

ユーザ登録時に、Emailによる「会員登録手続き」が行われます。  
その時、メール内の「本登録用URL」にそのまま飛んでも上手くページにアクセスすることが出来ません。  
現状、PORTが表示されていないのが原因となっています。  
PORT"1337"を指定し、「本登録用URL」にアクセスして下さい。  

 
