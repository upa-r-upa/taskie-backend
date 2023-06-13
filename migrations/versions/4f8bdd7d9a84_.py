"""empty message

Revision ID: 4f8bdd7d9a84
Revises: 
Create Date: 2023-06-14 03:08:41.215835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f8bdd7d9a84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=False),
    sa.Column('profile_image', sa.String(length=100), nullable=True),
    sa.Column('nickname', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('habit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('active', sa.Integer(), nullable=True),
    sa.Column('start_time_minutes', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('routine',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('start_time_minutes', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Integer(), nullable=True),
    sa.Column('active', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('habit_repeat_day',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('habit_id', sa.Integer(), nullable=False),
    sa.Column('day', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['habit_id'], ['habit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('habit_todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('habit_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['habit_id'], ['habit.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('routine_repeat_day',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('routine_id', sa.Integer(), nullable=False),
    sa.Column('day', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['routine_id'], ['routine.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('todo_routine',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('routine_id', sa.Integer(), nullable=False),
    sa.Column('todo_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('duration_minutes', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['routine_id'], ['routine.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['todo_id'], ['todo.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo_routine')
    op.drop_table('routine_repeat_day')
    op.drop_table('habit_todo')
    op.drop_table('habit_repeat_day')
    op.drop_table('todo')
    op.drop_table('routine')
    op.drop_table('habit')
    op.drop_table('user')
    # ### end Alembic commands ###
