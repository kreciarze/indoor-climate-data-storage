"""empty message

Revision ID: d261505ab3d8
Revises: 1a17a881184a
Create Date: 2024-01-23 16:18:52.755926

"""
import sqlalchemy as sa  # noqa: F401
from alembic import op  # noqa: F401

# revision identifiers, used by Alembic.
revision = "d261505ab3d8"
down_revision = "1a17a881184a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("device", "uuid", existing_type=sa.UUID(), nullable=False, schema="krecik_iot")
    op.create_unique_constraint(None, "device", ["uuid"], schema="krecik_iot")
    op.alter_column("activationrequest", "device_uuid", existing_type=sa.UUID(), nullable=False, schema="krecik_iot")
    op.drop_constraint("activationrequest_device_id_fkey", "activationrequest", schema="krecik_iot", type_="foreignkey")
    op.create_foreign_key(
        None,
        "activationrequest",
        "device",
        ["device_uuid"],
        ["uuid"],
        source_schema="krecik_iot",
        referent_schema="krecik_iot",
    )
    op.drop_column("activationrequest", "device_id", schema="krecik_iot")
    op.alter_column("record", "device_uuid", existing_type=sa.UUID(), nullable=False, schema="krecik_iot")
    op.drop_constraint("record_device_id_fkey", "record", schema="krecik_iot", type_="foreignkey")
    op.create_foreign_key(
        None,
        "record",
        "device",
        ["device_uuid"],
        ["uuid"],
        source_schema="krecik_iot",
        referent_schema="krecik_iot",
    )
    op.drop_column("record", "device_id", schema="krecik_iot")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "record",
        sa.Column("device_id", sa.INTEGER(), autoincrement=False, nullable=False),
        schema="krecik_iot",
    )
    op.drop_constraint(None, "record", schema="krecik_iot", type_="foreignkey")
    op.create_foreign_key(
        "record_device_id_fkey",
        "record",
        "device",
        ["device_id"],
        ["id"],
        source_schema="krecik_iot",
        referent_schema="krecik_iot",
    )
    op.alter_column("record", "device_uuid", existing_type=sa.UUID(), nullable=True, schema="krecik_iot")
    op.drop_constraint(None, "device", schema="krecik_iot", type_="unique")
    op.alter_column("device", "uuid", existing_type=sa.UUID(), nullable=True, schema="krecik_iot")
    op.add_column(
        "activationrequest",
        sa.Column("device_id", sa.INTEGER(), autoincrement=False, nullable=False),
        schema="krecik_iot",
    )
    op.drop_constraint(None, "activationrequest", schema="krecik_iot", type_="foreignkey")
    op.create_foreign_key(
        "activationrequest_device_id_fkey",
        "activationrequest",
        "device",
        ["device_id"],
        ["id"],
        source_schema="krecik_iot",
        referent_schema="krecik_iot",
    )
    op.alter_column("activationrequest", "device_uuid", existing_type=sa.UUID(), nullable=True, schema="krecik_iot")
    # ### end Alembic commands ###
