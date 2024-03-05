"""Initial migration.

Revision ID: 974f85c5698e
Revises:
Create Date: 2024-03-05 16:03:32.044091
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "974f85c5698e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "gate",
        sa.Column("station", sa.String(length=64), nullable=False),
        sa.Column(
            "state", sa.Enum("OPENED", "CLOSED", name="gatestate"), nullable=True
        ),
        sa.PrimaryKeyConstraint("station"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("gate")
    # ### end Alembic commands ###
