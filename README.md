# mediba-KPI

## ■ Description
以下ローカル開発環境構築（Mac）の手順について記載しています。Windows版が必要な場合は別途。  
「事前準備」は、それぞれについて未実施の方が実施してください。

## ■ 事前準備
* Virtual Boxをインストール
    * <https://www.virtualbox.org/wiki/Downloads>

* Vagrantをインストール
    * <http://www.vagrantup.com/downloads.html>

* HomeBrewをインストール
    * `` ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" ``

* Gitをインストール
    * `` brew install git ``

* Git SSH公開鍵設定
    * `` ssh-keygen -t rsa ``
        * すでに公開鍵を保持している場合は公開鍵の作成は不要
    * 上記で作成した公開鍵をGitに設定する。
        * `` cat ~/.ssh/id_rsa.pub | pbcopy ``で公開鍵がコピーされるので、下記に貼り付けする
        * <https://github.com/settings/ssh>

* ansibleをインストール
    * `` brew install ansible ``

## ■ 環境構築
* mediba-kpiをcloneする。  
（Git リポジトリのコピーを取得すること）  
（/path/toは任意のフォルダを指しています。各々でパスを読み替えて下さい。）
```
$ mkdir -p /path/to
$ cd /path/to
$ ssh-add ~/.ssh/id_rsa
$ git clone git@github.com:lochuynh-mediba/dmp-system.git
$ git checkout master
```

* Vagrantfileを編集し、コメントアウトを下記のように変更
    * バッチサーバ設定
```
node2.vm.synced_folder ".", "/vagrant", :owner=>"vagrant", :group=>"vagrant", :mount_options => ["dmode=777", "fmode=775"]
#node2.vm.synced_folder ".", "/vagrant", :owner=>"batch-mediba-kpi", :group=>"batch-mediba-kpi", :mount_options => ["dmode=777", "fmode=775"]
```

* ```$ vagrant up``` を実行


* プロビジョンが正常終了したら、Vagrantfileの中の下記項目のコメントアウトを入れ替える
    * バッチサーバ設定
```
#node2.vm.synced_folder ".", "/vagrant", :owner=>"vagrant", :group=>"vagrant", :mount_options => ["dmode=777", "fmode=775"]
node2.vm.synced_folder ".", "/vagrant", :owner=>"batch-medibakpi", :group=>"batch-medibakpi", :mount_options => ["dmode=777", "fmode=775"]
```

* ```$ vagrant reload``` を実行
（provisionは不要）

* 動作確認
  * ```$ vagrant ssh mediba_kpi_local_batch01``` で仮想バッチサーバにログイン
  * バッチユーザ（batch-mediba-kpi）にスイッチし、pythonバージョン確認とmysqlにログインできるかを確認
```
[vagrant@local-mediba-kpi-batch01 ~]$ sudo su - batch-medibakpi
[batch-mediba-kpi@local-mediba-kpi-batch01 ~]$ python -V
Python 3.6.0
[batch-mediba-kpi@local-mediba-kpi-batch01 ~]$ mysql -umedibakpi -p -h localhost medibakpi
Enter password: medibakpi
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.17 MySQL Community Server (GPL)

Copyright (c) 2000, 2016, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show tables;
Empty set (0.00 sec)

mysql> exit;
Bye
```
