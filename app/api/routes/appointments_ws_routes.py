from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import ALGORITHM, SECRET_KEY
from app.core.realtime import appointment_realtime_manager
from app.db.session import get_db
from app.models.user_model import User


router = APIRouter(tags=["Appointments WS"])


@router.websocket("/appointments/ws")
async def appointments_websocket(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")

        if not email or not role:
            await websocket.close(code=1008)
            return

        user = db.query(User).filter(User.email == email).first()
        if not user:
            await websocket.close(code=1008)
            return

        await appointment_realtime_manager.connect(
            websocket=websocket,
            role=role,
            email=email,
            programa_academico=user.programa_academico,
        )

        while True:
            await websocket.receive_text()
    except (JWTError, WebSocketDisconnect):
        appointment_realtime_manager.disconnect(websocket)
    except Exception:
        appointment_realtime_manager.disconnect(websocket)
        await websocket.close(code=1011)
