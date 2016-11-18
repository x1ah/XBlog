#!/usr/bin/env python
# coding:utf-8

import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from XBlog import create_app, db
from XBlog.models import User


app = create_app(os.getenv("XBLOG_CONFIG") or "default")
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
