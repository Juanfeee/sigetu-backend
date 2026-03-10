"""Repositorio de persistencia para citas activas e historial."""

from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.modelo_historial_cita import AppointmentHistory
from app.models.modelo_cita import Appointment
from app.models.modelo_usuario import User


class RepositorioCitas:
    """Encapsula consultas y escrituras de citas para reutilizar acceso a datos."""

    def crear(self, db: Session, cita: Appointment) -> Appointment:
        """Persiste una cita nueva y devuelve la entidad refrescada."""
        db.add(cita)
        db.commit()
        db.refresh(cita)
        return cita

    def obtener_por_id(self, db: Session, appointment_id: int) -> Appointment | None:
        """Obtiene una cita activa por identificador interno."""
        return db.query(Appointment).filter(Appointment.id == appointment_id).first()

    def obtener_por_id_estudiante(self, db: Session, student_id: int) -> list[Appointment]:
        """Lista citas activas de un estudiante ordenadas por fecha de creación."""
        return (
            db.query(Appointment)
            .filter(Appointment.student_id == student_id)
            .order_by(Appointment.created_at.desc())
            .all()
        )

    def obtener_historial_por_id_estudiante(self, db: Session, student_id: int) -> list[AppointmentHistory]:
        """Lista citas archivadas de un estudiante en orden descendente."""
        return (
            db.query(AppointmentHistory)
            .filter(
                AppointmentHistory.student_id == student_id,
            )
            .order_by(AppointmentHistory.archived_at.desc())
            .all()
        )

    def obtener_actuales_por_id_estudiante(self, db: Session, student_id: int) -> list[Appointment]:
        """Retorna citas en curso del estudiante para la vista de estado actual."""
        return (
            db.query(Appointment)
            .filter(
                Appointment.student_id == student_id,
                Appointment.status.in_(["pendiente", "llamando", "en_atencion"]),
            )
            .order_by(Appointment.created_at.desc())
            .all()
        )

    def obtener_cola(self, db: Session, sede: str, programa_academico: str | None = None) -> list[Appointment]:
        """Consulta la cola activa por sede con filtro opcional por programa académico."""
        consulta = (
            db.query(Appointment)
            .join(User, Appointment.student_id == User.id)
            .filter(
                Appointment.sede == sede,
                Appointment.status.in_(["pendiente", "llamando", "en_atencion"]),
            )
            .order_by(Appointment.created_at.asc())
        )

        if programa_academico is not None:
            consulta = consulta.filter(User.programa_academico == programa_academico)

        return consulta.all()

    def obtener_historial_cola(self, db: Session, sede: str, secretaria_id: int | None = None) -> list[AppointmentHistory]:
        """Consulta historial por sede y, cuando aplica, por usuario staff responsable."""
        consulta = (
            db.query(AppointmentHistory)
            .join(User, AppointmentHistory.student_id == User.id)
            .filter(
                AppointmentHistory.sede == sede,
            )
            .order_by(AppointmentHistory.archived_at.desc())
        )

        if secretaria_id is not None:
            consulta = consulta.filter(AppointmentHistory.secretaria_id == secretaria_id)

        return consulta.all()

    def actualizar_estado(self, db: Session, cita: Appointment, status: str) -> Appointment:
        """Actualiza estado de una cita activa y confirma transacción."""
        cita.status = status
        db.commit()
        db.refresh(cita)
        return cita

    def archivar_y_eliminar(
        self,
        db: Session,
        cita: Appointment,
        estado_final: str,
        secretaria_id: int | None = None,
        attention_ended_at=None,
        scheduled_at_historial=None,
    ) -> AppointmentHistory:
        """Mueve una cita a historial y elimina el registro activo en una sola operación."""
        historial = AppointmentHistory(
            appointment_id=cita.id,
            student_id=cita.student_id,
            secretaria_id=secretaria_id,
            sede=cita.sede,
            category=cita.category,
            context=cita.context,
            status=estado_final,
            turn_number=cita.turn_number,
            created_at=cita.created_at,
            scheduled_at=scheduled_at_historial if scheduled_at_historial is not None else cita.scheduled_at,
            attention_started_at=cita.attention_started_at,
            attention_ended_at=attention_ended_at,
            student=cita.student,
        )
        db.add(historial)
        db.delete(cita)
        db.commit()
        db.refresh(historial)
        return historial

    def actualizar(self, db: Session, cita: Appointment, **campos) -> Appointment:
        """Aplica actualización parcial de campos permitidos sobre una cita."""
        for nombre_campo, valor_campo in campos.items():
            if valor_campo is not None:
                setattr(cita, nombre_campo, valor_campo)
        db.commit()
        db.refresh(cita)
        return cita

    def siguiente_secuencia_turno(self, db: Session, sede: str, para_fecha: date) -> int:
        """Calcula el siguiente consecutivo diario de turnos considerando activos e historial."""
        turnos_activos = (
            db.query(Appointment.turn_number)
            .filter(
                Appointment.sede == sede,
                func.date(Appointment.created_at) == para_fecha,
            )
            .all()
        )

        turnos_historial = (
            db.query(AppointmentHistory.turn_number)
            .filter(
                AppointmentHistory.sede == sede,
                func.date(AppointmentHistory.created_at) == para_fecha,
            )
            .all()
        )

        max_secuencia = 0
        for tupla_turno in [*turnos_activos, *turnos_historial]:
            numero_turno = tupla_turno[0]
            if not numero_turno:
                continue

            partes = numero_turno.split("-")
            if len(partes) != 3:
                continue

            try:
                secuencia = int(partes[2])
            except ValueError:
                continue

            if secuencia > max_secuencia:
                max_secuencia = secuencia

        return max_secuencia + 1
