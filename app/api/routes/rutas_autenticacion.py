"""Endpoints HTTP para registro, login y manejo de tokens de autenticación."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.esquema_usuarios import RespuestaAuth, CrearUsuario, RespuestaCierreSesion, SolicitudRenovarToken, RespuestaRenovarToken, SolicitudLogin, RespuestaUsuario, SolicitudInvitado, RespuestaInvitado
from app.core.dependencias_autenticacion import obtener_payload_token_actual
from app.models.modelo_usuario import User
from app.db.sesion import obtener_db
from app.services.servicio_autenticacion import ServicioAutenticacion


router = APIRouter(prefix="/auth", tags=["Auth"])
servicio_auth = ServicioAutenticacion()


@router.post("/register", response_model=RespuestaAuth)
def registrar(datos_usuario: CrearUsuario, device_id: str | None = None, db: Session = Depends(obtener_db)):
    """Registra un usuario estudiante y devuelve perfil junto con tokens JWT."""
    return servicio_auth.registrar(
        db=db,
        full_name=datos_usuario.full_name,
        email=datos_usuario.email,
        password=datos_usuario.password,
        programa_academico=datos_usuario.programa_academico,
        device_id=device_id,
    )


@router.post("/login", response_model=RespuestaAuth)
def iniciar_sesion(datos_login: SolicitudLogin, db: Session = Depends(obtener_db)):
    """Autentica credenciales de usuario y entrega access/refresh token."""
    return servicio_auth.iniciar_sesion(
        db=db,
        email=datos_login.email,
        password=datos_login.password,
    )


@router.post("/guest", response_model=RespuestaInvitado)
def login_invitado(solicitud: SolicitudInvitado):
    """Genera token de acceso temporal para flujo de invitado."""
    return servicio_auth.login_invitado(device_id=solicitud.device_id)


@router.post("/refresh", response_model=RespuestaRenovarToken)
def renovar_token(carga: SolicitudRenovarToken, db: Session = Depends(obtener_db)):
    """Renueva par de tokens usando un refresh token válido."""
    return servicio_auth.renovar(
        db=db,
        refresh_token=carga.refresh_token,
    )


@router.post("/logout", response_model=RespuestaCierreSesion)
def cerrar_sesion(carga: SolicitudRenovarToken, db: Session = Depends(obtener_db)):
    """Revoca refresh token para cerrar sesión del cliente."""
    return servicio_auth.cerrar_sesion(
        db=db,
        refresh_token=carga.refresh_token,
    )


@router.get("/me", response_model=RespuestaUsuario)
def obtener_mi_perfil(
    db: Session = Depends(obtener_db),
    carga_token: dict = Depends(obtener_payload_token_actual),
):
    """Retorna datos del usuario autenticado por token de acceso."""
    usuario = db.query(User).filter(User.email == carga_token["sub"]).first()
    if not usuario:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario