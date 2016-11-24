这是一个Python+Flask写的博客网站, 可以在 [http://123.207.240.106/](http://123.207.240.106) 预览
还在完善中

FEATURES:
- Login
- New Post
- Edit Post
- Remove Post

TODO:
- 留言板
- 评论

Usage:
```python
# requitment: python2, virtualenv
$ source venv/bin/activate
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
$ python manage.py runserver
# open "http://localhost:5000"
```
