from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth_dependencies import require_student_role
from app.db.session import get_db
from app.schemas.appointment_schema import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointments"])
service = AppointmentService()


@router.post("", response_model=AppointmentResponse)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(require_student_role),
):
    return service.create_appointment(db=db, payload=payload, student_email=token_payload["sub"])


@router.get("/me", response_model=list[AppointmentResponse])
def get_my_appointments(
    db: Session = Depends(get_db),
    token_payload: dict = Depends(require_student_role),
):
    return service.get_student_appointments(db=db, student_email=token_payload["sub"])


@router.get("/me/current", response_model=list[AppointmentResponse])
def get_my_current_appointments(
    db: Session = Depends(get_db),
    token_payload: dict = Depends(require_student_role),
):
    return service.get_student_current_appointments(db=db, student_email=token_payload["sub"])


@router.get("/me/history", response_model=list[AppointmentResponse])
def get_my_appointment_history(
    db: Session = Depends(get_db),
    token_payload: dict = Depends(require_student_role),
):
    return service.get_student_appointment_history(db=db, student_email=token_payload["sub"])


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def update_my_appointment(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(require_student_role),
):
    return service.update_student_appointment(
        db=db,
        appointment_id=appointment_id,
        payload=payload,
        student_email=token_payload["sub"],
    )


@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_my_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(require_student_role),
):
    return service.cancel_student_appointment(
        db=db,
        appointment_id=appointment_id,
        student_email=token_payload["sub"],
    )
