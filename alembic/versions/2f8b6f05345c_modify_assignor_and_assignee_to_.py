"""Modify assignor and assignee to ForeignKey

Revision ID: 2f8b6f05345c
Revises: a13ae34409bc
Create Date: 2025-03-04 16:59:12.782383

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '2f8b6f05345c'
down_revision: Union[str, None] = 'a13ae34409bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "new_users",
        sa.Column("user_id", sa.String(36), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    op.execute("""
        INSERT INTO new_users (user_id, username, email, hashed_password, role) 
        SELECT user_id, username, email, hashed_password, role FROM users
    """)

    op.drop_table("users")
    op.rename_table("new_users", "users")

    op.create_table(
        "new_tasks",
        sa.Column("task_id", sa.String(36), primary_key=True, nullable=False),
        sa.Column('task_name', sa.VARCHAR(length=50), nullable=False),
        sa.Column('task_description', sa.TEXT(), nullable=False),
        sa.Column("assignee", sa.String(36), sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column("assignor", sa.String(36), sa.ForeignKey("users.user_id"), nullable=False),
        sa.Column('start_date', sa.DATE(), nullable=False),
        sa.Column('end_date', sa.DATE(), nullable=False),
        sa.Column('task_deadline', sa.DATE(), nullable=False),
        sa.Column('completed', sa.BOOLEAN(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="Pending"),
        sa.Column("feedback", sa.String(), nullable=True, server_default=""),
        sa.PrimaryKeyConstraint('task_id'),
        sa.UniqueConstraint('task_id'),
        sa.UniqueConstraint('task_name')
    )

    op.execute("""
        INSERT INTO new_tasks (task_id, task_name, task_description, assignee, assignor, start_date, end_date, task_deadline, completed) 
        SELECT task_id, task_name, task_description, assignee, assignor, start_date, end_date, task_deadline, completed FROM tasks
    """)

    op.drop_table("tasks")
    op.rename_table("new_tasks", "tasks")

def downgrade() -> None:
    op.drop_constraint("tasks_assignee_fkey", "tasks", type_="foreignkey")
    op.drop_constraint("tasks_assignor_fkey", "tasks", type_="foreignkey")

    op.alter_column('tasks', 'assignor',
            existing_type=sa.String(length=36),
            type_=sa.String(length=50),
            existing_nullable=False)
    op.alter_column('tasks', 'assignee',
            existing_type=sa.String(length=36),
            type_=sa.String(length=50),
            existing_nullable=False)
