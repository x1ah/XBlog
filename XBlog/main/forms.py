#!/usr/bin/env python
# coding:utf-8

from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField

from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms import BooleanField, SelectField, ValidationError
from wtforms.validators import Required, Length, Regexp, Email, URL


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        Required(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[Required()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")


class EditAbout(FlaskForm):
    about = PageDownField("ABOUT")
    submit = SubmitField("Submit")


class EditPostForm(FlaskForm):
    title = StringField("Title", validators=[Required()])
    categories = StringField("Category", validators=[Required(), Length(1, 64)])
    nature = SelectField(u"type", coerce=str)
    about_this_article = PageDownField("About this article", validators=[Required()])
    body = PageDownField("WRITE", validators=[Required()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)

        self.nature.choices = [("tecnology", u"技术"), ("life", u"生活")]


class LeaveMessageForm(FlaskForm):
    user_name = StringField(u"昵称(英文)*:", validators=[
        Required(),
        Length(1, 64), Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
                              "Usernames must have only letters, "
                              "numbers, dots or underscores")
    ])
    user_email = StringField(u"邮箱(非必须)", validators=[Email()])
    user_site = StringField(u"您的主页(http://example.com)*", validators=[Length(1, 64), URL()])
    body = PageDownField(u"您的留言*", validators=[Required(), Length(1, 200)])
    submit = SubmitField(u"提交")
