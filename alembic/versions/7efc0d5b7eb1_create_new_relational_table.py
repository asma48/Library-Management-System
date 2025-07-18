"""create new relational table

Revision ID: 7efc0d5b7eb1
Revises: db2856bc5188
Create Date: 2025-07-03 01:10:58.174565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7efc0d5b7eb1'
down_revision: Union[str, Sequence[str], None] = 'db2856bc5188'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrower_book', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('borrower_book', sa.Column('create_at', sa.DateTime(), nullable=True))
    op.add_column('borrower_book', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('borrower_book', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('borrower_book', sa.Column('deleted_by', sa.String(), nullable=True))
    op.create_index(op.f('ix_borrower_book_book_id'), 'borrower_book', ['book_id'], unique=False)
    op.create_index(op.f('ix_borrower_book_borrower_id'), 'borrower_book', ['borrower_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_borrower_book_borrower_id'), table_name='borrower_book')
    op.drop_index(op.f('ix_borrower_book_book_id'), table_name='borrower_book')
    op.drop_column('borrower_book', 'deleted_by')
    op.drop_column('borrower_book', 'deleted_at')
    op.drop_column('borrower_book', 'updated_at')
    op.drop_column('borrower_book', 'create_at')
    op.drop_column('borrower_book', 'id')
    # ### end Alembic commands ###
