"""empty message

Revision ID: b963cd31f06c
Revises: None
Create Date: 2016-11-24 22:35:41.283910

"""

# revision identifiers, used by Alembic.
revision = 'b963cd31f06c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('about_me',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('posts', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['posts'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_timestamp'), 'categories', ['timestamp'], unique=False)
    op.create_table('leaving_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=64), nullable=True),
    sa.Column('user_email', sa.String(length=64), nullable=True),
    sa.Column('user_site', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('nature', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('body_html', sa.Text(), nullable=True),
    sa.Column('about_this_article', sa.Text(), nullable=True),
    sa.Column('about_this_article_html', sa.Text(), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('categories', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['users.id'], ),
    sa.ForeignKeyConstraint(['categories'], ['categories.category_name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_timestamp'), 'posts', ['timestamp'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_posts_timestamp'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('leaving_message')
    op.drop_index(op.f('ix_categories_timestamp'), table_name='categories')
    op.drop_table('categories')
    op.drop_table('about_me')
    ### end Alembic commands ###
