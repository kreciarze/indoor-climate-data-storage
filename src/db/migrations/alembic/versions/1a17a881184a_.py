"""empty message

Revision ID: 1a17a881184a
Revises: f5e0019c1e98
Create Date: 2024-01-23 15:57:59.212564

"""
import uuid

import sqlalchemy as sa  # noqa: F401
from alembic import op  # noqa: F401

from db.models.device import Device

# revision identifiers, used by Alembic.
revision = "1a17a881184a"
down_revision = "f5e0019c1e98"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("activationrequest", sa.Column("device_uuid", sa.UUID(), nullable=True), schema="krecik_iot")
    op.add_column("device", sa.Column("uuid", sa.UUID(), nullable=True), schema="krecik_iot")
    op.add_column("record", sa.Column("device_uuid", sa.UUID(), nullable=True), schema="krecik_iot")

    connection = op.get_bind()
    rows_to_update = connection.execute(sa.select(Device)).fetchall()
    for row in rows_to_update:
        op.execute(f"UPDATE krecik_iot.device SET uuid = '{uuid.uuid4()}' WHERE id = {row.id}")  # noqa: S608
    op.execute(
        "UPDATE krecik_iot.record "
        "SET device_uuid = (SELECT uuid FROM krecik_iot.device WHERE device.id = record.device_id)",
    )
    op.execute(
        "UPDATE krecik_iot.activationrequest "
        "SET device_uuid = (SELECT uuid FROM krecik_iot.device WHERE device.id = activationrequest.device_id)",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("record", "device_uuid", schema="krecik_iot")
    op.drop_column("device", "uuid", schema="krecik_iot")
    op.drop_column("activationrequest", "device_uuid", schema="krecik_iot")
    # ### end Alembic commands ###
