#!/usr/bin/env python
# encoding: utf-8

from XBlog.models import User
from manage import app

if __name__ == "__main__":
    with app.app_context():
        User.init_admin()
