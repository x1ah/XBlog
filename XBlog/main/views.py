from datetime import datetime
from collections import Counter
from flask import render_template, request, flash, redirect, url_for, current_app, abort
from flask_login import login_required, current_user
from . import main
from ..models import Post, About, Category, LevMessage
from .. import db
from .forms import EditPostForm, EditAbout, LeaveMessageForm

# =========================
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required

@main.route("/", methods=["GET", "PSOT"])
def index():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.filter_by(nature="tecnology").order_by(
        Post.timestamp.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"],
        error_out=False)
    posts = pagination.items
    return render_template("index.html", current_time=datetime.utcnow(),
                           posts=posts,
                           pagination=pagination,
                           Category=Category)


@main.route("/life")
def life():
    all_category = Category.query.all()
    categories = Counter([item.category_name for item in all_category])
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.filter_by(nature="life").order_by(
        Post.timestamp.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"],
        error_out=False)
    posts = pagination.items
    return render_template("index.html", current_time=datetime.utcnow(),
                           request=request, posts=posts, categories=categories,
                           pagination=pagination, Category=Category, life=True)


@main.route("/category/<categy>")
def category(categy):
    all_category = Category.query.all()
    categories = Counter([item.category_name for item in all_category])
    page = request.args.get("page", 1, type=int)
    pagination = Category.query.filter_by(category_name=categy).order_by(
        Category.timestamp.desc()).paginate(
        page, per_page=current_app.config["POSTS_PER_PAGE"],
        error_out=False)
    posts_id = [item.posts for item in pagination.items]
    posts = [Post.query.get_or_404(pid) for pid in posts_id]
    if posts is None:
        abort(404)
    return render_template("category.html", current_time=datetime.utcnow(),
                           request=request, posts=posts, categories=categories,
                           pagination=pagination, Category=Category)

@main.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = EditPostForm()
    if form.validate_on_submit():
        post = Post()
        post.title = form.title.data
        post.nature = form.nature.data
        post.categories = form.categories.data
        post.about_this_article = form.about_this_article.data
        post.body = form.body.data
        post.timestamp = datetime.utcnow()
        post.author = current_user._get_current_object().id
        db.session.add(post)
        db.session.commit()
        post_id = len(Post.query.all())
        categories = [item.strip() for item in form.categories.data.split(",")]
        for category in categories:
            categy = Category()
            categy.category_name = category
            categy.posts = post_id
            db.session.add(categy)
        db.session.commit()

        flash("Publish succeed.")
        return redirect(url_for("main.index"))
    return render_template("edit_post.html", form=form)


@main.route("/post/<int:pid>", methods=["GET", "POST"])
def post(pid):
    _post = Post.query.get_or_404(pid)
    # form = CommentForm()
    # if form.validate_on_submit():
    #     comment = Comment(body=form.body.data,
    #                       post=post,
    #                       author=current_user._get_current_object())
    #     db.session.add(comment)
    #     flash("Your comment has been published.")
    #     return redirect(url_for("main.post", id=post.id, page=-1))
    # page = request.args.get("page", 1, type=int)
    # if page == -1:
    #     page = (post.comments.count() -1) / \
    #         current_app.config["X2EX_POSTS_PER_PAGE"] + 1
    # pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
    #     page, per_page=current_app.config["X2EX_POSTS_PER_PAGE"],
    #     error_out=False)
    # comments = pagination.items
    return render_template("post.html", posts=[_post], Category=Category) # , form=form,
    #                        comments=comments, pagination=pagination)


@main.route("/about")
def about():
    about_me = About.query.first()
    return render_template("about.html", about=about_me, user=current_user,
                           admin=current_app.config.get("ADMIN"))


@main.route("/edit/<int:pid>", methods=["GET", "POST"])
@login_required
def edit(pid):
    post = Post.query.get_or_404(pid)
    form = EditPostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data
        post.nature = form.nature.data
        post.categories = form.categories.data
        post.timestamp = datetime.utcnow()
        post.author = current_user._get_current_object().id
        db.session.add(post)
        flash("The post has been updated.")
        return redirect(url_for("main.post", pid=post.id))
    form.title.data = post.title
    form.nature.data = post.nature
    form.categories.data = post.categories
    form.about_this_article.data = post.about_this_article
    form.body.data = post.body
    return render_template("edit_post.html", form=form)


@main.route("/delete/<int:pid>")
@login_required
def delete(pid):
    p = Post.query.filter_by(id=pid).first()
    db.session.delete(p)
    db.session.commit()
    category = Category.query.filter_by(posts=pid).all()
    for ca in category:
        db.session.delete(ca)
        db.session.commit()
    flash("You have delete the article!")
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route("/edabout", methods=["GET", "POST"])
@login_required
def edabout():
    about = About.query.filter_by(user=current_user.id).first()
    about = About() if about is None else about
    form = EditAbout()
    if form.validate_on_submit():
        about.body = form.about.data
        about.user = current_user.id
        db.session.add(about)
        return redirect(url_for("main.about"))
    form.about.data = about.body
    return render_template("edit_about.html", form=form)

@main.route("/message_board", methods=["GET", "POST"])
def message_board():
    form = LeaveMessageForm()
    page = request.args.get("page", 1, type=int)
    pagination = LevMessage.query.order_by(
        LevMessage.timestamp.desc()).paginate(
        page, per_page=current_app.config["LEVMEG_PER_PAGE"],
        error_out=False)
    msg = pagination.items
    if form.validate_on_submit():
        Message = LevMessage()
        Message.user_name = form.user_name.data
        Message.user_email = form.user_email.data
        Message.user_site = form.user_site.data
        Message.timestamp = datetime.utcnow()
        Message.message = form.body.data
        db.session.add(Message)
        return redirect(url_for("main.message_board"))
    return render_template("message_board.html",
                           msg=msg,
                           form=form,
                           pagination=pagination)
