"""zxc1

Revision ID: e06eb48ba6ff
Revises: 271fcfae4522
Create Date: 2024-04-03 19:01:06.690911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e06eb48ba6ff'
down_revision: Union[str, None] = '271fcfae4522'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('email', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'Users', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Users', type_='unique')
    op.drop_column('Users', 'email')
    # ### end Alembic commands ###
