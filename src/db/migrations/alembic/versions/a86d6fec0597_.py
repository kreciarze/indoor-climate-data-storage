"""empty message

Revision ID: a86d6fec0597
Revises: 3c5318f1a20f
Create Date: 2024-01-21 21:09:26.771675

"""
import sqlalchemy as sa  # noqa: F401
from alembic import op  # noqa: F401

# revision identifiers, used by Alembic.
revision = "a86d6fec0597"
down_revision = "3c5318f1a20f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("device", sa.Column("serial_number", sa.String(), nullable=True), schema="krecik_iot")
    op.add_column("device", sa.Column("activated", sa.Boolean(), nullable=True), schema="krecik_iot")
    op.alter_column("device", "user_id", existing_type=sa.INTEGER(), nullable=True, schema="krecik_iot")
    op.alter_column("device", "name", existing_type=sa.VARCHAR(), nullable=True, schema="krecik_iot")
    op.alter_column("device", "key", existing_type=sa.VARCHAR(), nullable=True, schema="krecik_iot")
    op.drop_constraint("device_serial_number_value_fkey", "device", schema="krecik_iot", type_="foreignkey")
    op.drop_column("device", "serial_number_value", schema="krecik_iot")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "device",
        sa.Column("serial_number_value", sa.VARCHAR(), autoincrement=False, nullable=True),
        schema="krecik_iot",
    )
    op.create_foreign_key(
        "device_serial_number_value_fkey",
        "device",
        "serialnumber",
        ["serial_number_value"],
        ["value"],
        source_schema="krecik_iot",
        referent_schema="krecik_iot",
    )
    op.alter_column("device", "key", existing_type=sa.VARCHAR(), nullable=False, schema="krecik_iot")
    op.alter_column("device", "name", existing_type=sa.VARCHAR(), nullable=False, schema="krecik_iot")
    op.alter_column("device", "user_id", existing_type=sa.INTEGER(), nullable=False, schema="krecik_iot")
    op.drop_column("device", "activated", schema="krecik_iot")
    op.drop_column("device", "serial_number", schema="krecik_iot")
    # ### end Alembic commands ###
