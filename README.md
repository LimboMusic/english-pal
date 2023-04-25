# EnglishPal - Learn English Words Smartly



Hui Lan <hui.lan@cantab.net>

1 November 2019


## What is it?


EnglishPal allows the user to build his list of new English words
picked from articles selected for him to read according his vocabulary level.  EnglishPal will determine a user's vocabulary level based on his picked words.  After that, it will recommend articles for him to read, in order to booster his English vocabulary furthermore.


## Run on your own laptop

`python3 main.py`

Make sure you have put the SQLite database file in the path `app/static` (see below).


## Run it as a Docker container


Assuming that docker has been installed and that you are a sudo user (i.e., sudoer), start the program by typing the following command in directory `EnglishPal`:

`sudo ./build.sh`

Open your favourite Internet browser and enter this URL address: `http://ip-address:90`.  Note: you must update the variable `DEPLOYMENT_DIR` in `build.sh`.

### Explanation on the commands in build.sh

My steps for deploying English on a Ubuntu server.

- ssh to ubuntu@118.*.*.118

- cd to `/home/lanhui/englishpal2/EnglishPal`

- Stop all docker service: `sudo service docker restart`.  If you know the docker container ID, then the above command is an overkill.  Use the following command instead: `sudo docker stop ContainerID`.  You could get all container IDs with the following command: `sudo docker ps`

- Rebuild container. Run the following command to rebuild a docker image each time after the source code gets updated: `sudo docker build -t englishpal .`

- Run the application: `sudo docker run -d -p 90:80 -v /home/lanhui/englishpal2/EnglishPal/app/static/frequency:/app/static/frequency -t englishpal`. If you use `sudo docker run -d -p 90:80 -t englishpal`, data will be lost after terminating the program.  If you want to automatically restart the docker image after each system reboot, add the option `--restart=always` after `docker run`.

- Save disk space: `sudo docker system prune -a -f`

`build.sh` contains all the above commands.  Run "sudo ./build.sh" to rebuild and start the web application.


#### Other useful docker commands

- `sudo docker ps -a`

- `sudo docker logs image_name`, where `image_name` could be obtained from `sudo docker ps`.



## Importing articles


All articles are stored in the `article` table in a SQLite file called
`app/static/wordfreqapp.db`.

### Adding new articles

To add articles, open and edit `app/static/wordfreqapp.db` using DB Browser for SQLite (https://sqlitebrowser.org).

### Extending an account's expiry date

By default, an account's expiry is 30 days after first sign-up.  To extend account's expiry date, open and edit `user` table in `app/static/wordfreqapp.db`.  Simply update field `expiry_date`.

### Exporting the database

Export wordfreqapp.db to wordfreqapp.sql using the following commands:

- sqlite3 wordfreqapp.db

- .output wordfreqapp.sql

- .dump

- .exit

Put wordfreqapp.sql (not wordfreqapp.db) under version control.

### Creating SQLite file from wordfreqapp.sql


Create wordfreqapp.db using this command: `cat wordfreqapp.sql |
sqlite3 wordfreqapp.db`.  Delete wordfreqapp.db first if it exists.


### Uploading wordfreqapp.db to the server


`pscp wordfreqapp.db lanhui@118.*.*.118:/home/lanhui/englishpal2/EnglishPal/app/static`



## Feedback

We welcome feedback on EnglishPal.  Feedback examples:

### Feedback 1

- "Need a phone app.  I use phone a lot.  You cannot ask students to use computers."


### Feedback 2


- “成为会员”改成“注册”

- “登出”改成“退出”

- “收集生词吧”改成“生词收集栏”

- 不要自动显示下一篇

- 需要有“上一篇”、“下一篇”按钮。



## Bug tracking


EnglishPal's bugs and improvement suggestions are recorded in [Bugzilla](http://118.25.96.118/bugzilla/buglist.cgi?bug_status=__all__&list_id=1302&order=Importance&product=EnglishPal&query_format=specific).  Send (lanhui at zjnu.edu.cn) an email message for opening a Bugzilla account or reporting a bug.



## TODO


- Fix Bug: Internal server error when register using an email address.

- Usability testing


## Improvements made by contributors (incomplete list)


### 朱文绮


在生词簿每个单词后面，加上两个按钮，熟悉与不熟悉:

- 如果点熟悉，就将生词簿中该单词后面记录的添加次数减一，直至减为0，就将该单词从生词簿中移除。

- 如果点不熟悉，就将生词簿中该单词后面记录的添加次数加一。

### 李康恬


Add the function of "Delete already known and well-known words from
the words' library", on the one hand, it can conform to the usage
habits of some users, who do not like that their words' libraries have
too many words that they already know, on the other hand, it can
reduce unnecessary memory occupied by the database, in addition, it
can also improve the simplicity of the page.



### 占健豪


Click the Familiar or Unfamiliar button (current word frequency>1), the current word position is displayed at the top of the page;

Click the Familiar or Unfamiliar button (current word frequency is 1), and the page will be displayed as the top of the entire page.

Demo video link: https://b23.tv/QuB77m

### 张小飞


修复了以下漏洞。

漏洞：用 `‘ or ‘1’=‘1’` 这段字符可以作为任何账号的密码登录。

Bug report: http://118.25.96.118/bugzilla/show_bug.cgi?id=215




### 丁锐

修复了以下漏洞

漏洞：新用户在创建账号时，不需要输入确定密码也可以注册成功，并且新账户可以正常使用。

Bug report: http://118.25.96.118/bugzilla/show_bug.cgi?id=489


*Last modified on 2023-01-30*

