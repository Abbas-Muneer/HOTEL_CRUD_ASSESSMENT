"""add hotel status"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0002_add_hotel_status"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "hotels",
        sa.Column(
            "status", sa.String(length=50), nullable=False, server_default="active"
        ),
    )
    op.create_index("ix_hotels_status", "hotels", ["status"])


def downgrade():
    op.drop_index("ix_hotels_status", table_name="hotels")
    op.drop_column("hotels", "status")
