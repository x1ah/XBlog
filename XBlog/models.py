#!/usr/bin/env python
# coding:utf-8

from datetime import datetime

import bleach
from flask import current_app
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(64))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config.get("SECRET_KEY"), expiration=expiration)
        return s.dumps({"reset", self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config.get("SECRET_KEY"))
        try:
            data = s.loads(token)
        except:
            return False
        if data.get("reset") != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    @staticmethod
    def init_admin():
        db.create_all()
        u = User()
        u.email = current_app.config.get("ADMIN")
        u.password = current_app.config.get("ADMIN_PASSWORD")
        db.session.add(u)
        db.session.commit()

class About(db.Model):
    __tablename__ = "about_me"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    user = db.Column(db.Integer, db.ForeignKey("users.id"))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ["a", "abbr", "acronym", "b", "blockquote", "code",
                        "em", "i", "li", "ol", "pre", "strong", "ul", "h1",
                        "h2", "h3", "p", "span", "br"]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format="html"),
            tags=allowed_tags))


db.event.listen(About.body, "set", About.on_changed_body)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    posts = db.Column(db.Integer, db.ForeignKey("posts.id"))


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    nature = db.Column(db.String(64))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    body_html = db.Column(db.Text)
    about_this_article = db.Column(db.Text)
    about_this_article_html = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey("users.id"))
    categories = db.Column(db.String(64), db.ForeignKey("categories.category_name"))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body_html = markdown(value, output_format="html")

    @staticmethod
    def on_changed_about(target, value, oldvalue, initiator):
        target.about_this_article_html = markdown(value, output_format="html")


db.event.listen(Post.about_this_article, "set", Post.on_changed_about)
db.event.listen(Post.body, "set", Post.on_changed_body)


class LevMessage(db.Model):
    __tablename__ = "leaving_message"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64))
    user_email = db.Column(db.String(64))
    user_site = db.Column(db.String(64))

class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser
