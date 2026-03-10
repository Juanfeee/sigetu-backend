"""Esquemas Pydantic para operaciones de citas, cola e historial."""

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints


TipoCategoria = Literal[
    "academico",
    "administrativo",
    "financiero",
    "otro",
    "pagos_facturacion",
    "recibos_certificados",
    "creditos_financiacion",
    "problemas_soporte_financiero",
    "plataformas_servicios",
    "informacion_academica",
    "inscripcion_matricula",
]
TipoEstado = Literal["pendiente", "llamando", "en_atencion", "atendido", "no_asistio", "cancelada"]


class CrearCita(BaseModel):
    """Datos requeridos para crear una cita en una sede determinada."""
    category: TipoCategoria
    context: Annotated[str, StringConstraints(min_length=2, max_length=120, strip_whitespace=True)]
    scheduled_at: datetime | None = None


class ActualizarCita(BaseModel):
    """Payload parcial para editar una cita pendiente."""
    category: TipoCategoria | None = None
    context: Annotated[str, StringConstraints(min_length=2, max_length=120, strip_whitespace=True)] | None = None
    scheduled_at: datetime | None = None


class ActualizarEstadoCita(BaseModel):
    """Payload para transición de estado de una cita por staff."""
    status: TipoEstado


class InfoEstudianteCita(BaseModel):
    """Resumen del estudiante asociado a una cita."""
    id: int
    full_name: str
    email: str
    programa_academico: str | None = None


class RespuestaDetalleCita(BaseModel):
    """Respuesta detallada de cita para vistas operativas de staff."""
    id: int
    student_id: int | None
    device_id: str | None = None
    turn_number: str
    sede: str
    category: TipoCategoria
    context: str
    status: TipoEstado
    created_at: datetime
    scheduled_at: datetime | None = None
    attention_started_at: datetime | None = None
    student: InfoEstudianteCita | None = None


class HorarioOcupado(BaseModel):
    """Slot de agenda ocupado y posible fin estimado de atención."""
    scheduled_at: datetime
    status: TipoEstado
    attention_ends_at: datetime | None = None


class RespuestaHorariosOcupados(BaseModel):
    """Contenedor de horarios ocupados para un rango consultado."""
    horarios: list[HorarioOcupado]


class RespuestaExtenderTiempo(BaseModel):
    """Resultado de extensión de atención y total de citas afectadas."""
    mensaje: str
    citas_actualizadas: int


class RespuestaCita(BaseModel):
    """Representación estándar de cita activa en respuestas HTTP."""
    id: int
    student_id: int | None = None
    device_id: str | None = None
    student_name: str | None = None
    sede: str
    category: TipoCategoria
    context: str
    status: TipoEstado
    turn_number: str
    created_at: datetime
    scheduled_at: datetime | None = None
    attention_started_at: datetime | None = None

    class Config:
        from_attributes = True


class ItemColaCita(BaseModel):
    """Elemento resumido de cola o historial para listados."""
    id: int
    student_name: str | None = None
    secretaria_name: str | None = None
    turn_number: str
    category: TipoCategoria
    context: str
    status: TipoEstado
    created_at: datetime
    scheduled_at: datetime | None = None

    class Config:
        from_attributes = True
