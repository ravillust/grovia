"""Initial schema with users and detection_history tables

Revision ID: 3862c0cba6c3
Revises: 
Create Date: 2025-11-28 11:48:28.738839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3862c0cba6c3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial schema with users and detection_history tables."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('username', sa.String(255), nullable=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('is_superuser', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('verification_token', sa.String(255), nullable=True),
        sa.Column('reset_token', sa.String(255), nullable=True),
        sa.Column('reset_token_expires', sa.DateTime(), nullable=True),
        sa.Column('oauth_provider', sa.String(50), nullable=True),
        sa.Column('oauth_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_reset_token'), 'users', ['reset_token'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    
    op.create_table(
        'detection_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('disease_id', sa.String(100), nullable=False),
        sa.Column('disease_name', sa.String(150), nullable=False),
        sa.Column('scientific_name', sa.String(200), nullable=True),
        sa.Column('image_url', sa.String(500), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('description', sa.String(5000), nullable=True),
        sa.Column('symptoms', sa.String(5000), nullable=True),
        sa.Column('treatment', sa.Text(), nullable=True),
        sa.Column('detected_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_detection_history_id'), 'detection_history', ['id'], unique=False)
    op.create_index(op.f('ix_detection_history_user_id'), 'detection_history', ['user_id'], unique=False)


def downgrade() -> None:
    """Drop users and detection_history tables."""
    op.drop_index(op.f('ix_detection_history_user_id'), table_name='detection_history')
    op.drop_index(op.f('ix_detection_history_id'), table_name='detection_history')
    op.drop_table('detection_history')
    
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_reset_token'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
