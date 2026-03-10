"""agregar categorias admisiones mercadeo

Revision ID: c3d4e5f6a7b9
Revises: b2c3d4e5f6a8
Create Date: 2026-03-09 12:05:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c3d4e5f6a7b9"
down_revision: Union[str, Sequence[str], None] = "b2c3d4e5f6a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CATEGORY_CHECK_EXTENDIDO = (
    "category IN ('academico','administrativo','financiero','otro',"
    "'pagos_facturacion','recibos_certificados','creditos_financiacion',"
    "'problemas_soporte_financiero','plataformas_servicios',"
    "'informacion_academica','inscripcion_matricula')"
)

CATEGORY_CHECK_PREVIO = (
    "category IN ('academico','administrativo','financiero','otro',"
    "'pagos_facturacion','recibos_certificados','creditos_financiacion',"
    "'problemas_soporte_financiero','plataformas_servicios')"
)


def upgrade() -> None:
    with op.batch_alter_table("appointments") as batch_op:
        batch_op.drop_constraint("ck_appointments_category_valid", type_="check")
        batch_op.create_check_constraint("ck_appointments_category_valid", CATEGORY_CHECK_EXTENDIDO)

    with op.batch_alter_table("appointment_history") as batch_op:
        batch_op.drop_constraint("ck_appointment_history_category_valid", type_="check")
        batch_op.create_check_constraint("ck_appointment_history_category_valid", CATEGORY_CHECK_EXTENDIDO)


def downgrade() -> None:
    with op.batch_alter_table("appointment_history") as batch_op:
        batch_op.drop_constraint("ck_appointment_history_category_valid", type_="check")
        batch_op.create_check_constraint("ck_appointment_history_category_valid", CATEGORY_CHECK_PREVIO)

    with op.batch_alter_table("appointments") as batch_op:
        batch_op.drop_constraint("ck_appointments_category_valid", type_="check")
        batch_op.create_check_constraint("ck_appointments_category_valid", CATEGORY_CHECK_PREVIO)
