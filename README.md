这是一个Python+Flask+Material Design 写的博客网站, 可以在 [http://123.207.240.106/](http://123.207.240.106) 预览
还在完善中

技术栈
- 后端 Python + flask
- 前端 [Materialize](http://materializecss.com/)

FEATURES:
- 登录, 登出
- 登录后发布新博客
- 修改，删除
- 留言, 评论

TODO:
- 工具界面

或者本地预览效果
Usage:
```python
$ pip install -r requirements.txt
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ python manage.py shell
>>> User.init_admin()
>>> exit()
# default admin count: x1ahgxq@gmail.com
# default admin password: admin
# you can revise it in ./config.py but it will be replace by environment variable

$ python manage.py runserver
# open "http://localhost:5000"
```
