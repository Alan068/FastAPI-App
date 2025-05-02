"""Re-add status and feedback, fixing tasks db issue

Revision ID: b0da6d9c782c
Revises: 2f8b6f05345c
Create Date: 2025-03-05 10:15:12.123456

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b0da6d9c782c'
down_revision: Union[str, None] = '2f8b6f05345c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
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
        sa.Column("status", sa.String(20), nullable=False, server_default="Pending"),
        sa.Column("feedback", sa.String(200), nullable=True, server_default=""),
        sa.PrimaryKeyConstraint('task_id'),
        sa.UniqueConstraint('task_id'),
        sa.UniqueConstraint('task_name')
    )

    op.execute("""
    INSERT INTO new_tasks (task_id, task_name, task_description, assignee, assignor, start_date, end_date, task_deadline, completed, status, feedback) 
    SELECT task_id, task_name, task_description, assignee, assignor, start_date, end_date, task_deadline, completed, status, feedback FROM tasks
""")


    op.drop_table("tasks")
    op.rename_table("new_tasks", "tasks")


def downgrade() -> None:
    op.drop_column("tasks", "status")
    op.drop_column("tasks", "feedback")
