"""empty message

Revision ID: 2bce680e4d85
Revises: 1da03a8e88f1
Create Date: 2024-01-23 16:22:57.292236

"""
import sqlalchemy as sa  # noqa: F401
from alembic import op  # noqa: F401

# revision identifiers, used by Alembic.
revision = "2bce680e4d85"
down_revision = "1da03a8e88f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("device", "uuid", new_column_name="id", schema="krecik_iot")
    op.alter_column("record", "device_uuid", new_column_name="device_id", schema="krecik_iot")
    op.alter_column("activationrequest", "device_uuid", new_column_name="device_id", schema="krecik_iot")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("device", "id", new_column_name="uuid", schema="krecik_iot")
    op.alter_column("record", "device_id", new_column_name="device_uuid", schema="krecik_iot")
    op.alter_column("activationrequest", "device_id", new_column_name="device_uuid", schema="krecik_iot")
    # ### end Alembic commands ###
