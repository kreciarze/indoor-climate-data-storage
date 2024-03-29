"""empty message

Revision ID: 032f8567e10d
Revises: 2bce680e4d85
Create Date: 2024-01-23 16:28:52.438193

"""
import sqlalchemy as sa  # noqa: F401
from alembic import op  # noqa: F401

# revision identifiers, used by Alembic.
revision = "032f8567e10d"
down_revision = "2bce680e4d85"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("record_device_uuid_fkey", "record", schema="krecik_iot", type_="foreignkey")
    op.drop_constraint(
        "activationrequest_device_uuid_fkey",
        "activationrequest",
        schema="krecik_iot",
        type_="foreignkey",
    )
    op.drop_constraint("device_uuid_key", "device", schema="krecik_iot", type_="unique")

    op.create_primary_key("device_pkey", "device", ["id"], schema="krecik_iot")
    op.create_foreign_key(
        "record_device_id_fkey",
        "record",
        "device",
        ["device_id"],
        ["id"],
        source_schema="krecik_iot",
        referent_schema="krecik_iot",
    )
    op.create_foreign_key(
        "activationrequest_device_id_fkey",
        "activationrequest",
        "device",
        ["device_id"],
        ["id"],
        source_schema="krecik_iot",
        referent_schema="krecik_iot",
    )
    op.create_primary_key("activationrequest_pkey", "activationrequest", ["device_id"], schema="krecik_iot")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    raise NotImplementedError("Downgrade is not implemented")
    # ### end Alembic commands ###
