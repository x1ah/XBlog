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
    nature = SelectField(u"目录", coerce=str)
    about_this_article = PageDownField("About this article", validators=[Required()])
    body = PageDownField("WRITE", validators=[Required()])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)

        self.nature.choices = [("tecnology", u"技术"), ("life", u"生活")]


class LeaveMessageForm(FlaskForm):
    user_name = StringField("Your nick name:", validators=[
        Required(),
        Length(1, 64), Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
                              "Usernames must have only letters, "
                              "numbers, dots or underscores")
    ])
    user_email = StringField("Your email(not necessity)", validators=[Email()])
    user_site = StringField("Your website", validators=[Length(1, 64), URL()])
    body = PageDownField("Message", validators=[Required(), Length(1, 200)])
    submit = SubmitField("Submit")