from fastapi import WebSocket


class AppointmentRealtimeManager:
    def __init__(self) -> None:
        self._connections: list[dict] = []

    async def connect(self, websocket: WebSocket, role: str, email: str, programa_academico: str | None) -> None:
        await websocket.accept()
        self._connections.append(
            {
                "websocket": websocket,
                "role": role,
                "email": email,
                "programa_academico": programa_academico,
            }
        )

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections = [item for item in self._connections if item["websocket"] is not websocket]

    async def publish_appointment_event(self, event_type: str, appointment) -> None:
        student = getattr(appointment, "student", None)
        student_program = getattr(student, "programa_academico", None)
        student_email = getattr(student, "email", None)

        payload = {
            "event": event_type,
            "appointment": {
                "id": appointment.id,
                "status": appointment.status,
                "turn_number": appointment.turn_number,
                "student_id": appointment.student_id,
                "student_name": getattr(student, "full_name", None),
                "programa_academico": student_program,
            },
        }

        stale_connections = []

        for item in self._connections:
            role = item["role"]
            email = item["email"]
            programa = item["programa_academico"]
            websocket: WebSocket = item["websocket"]

            can_receive = False

            if role == "admin":
                can_receive = True
            elif role == "secretaria" and programa is not None and student_program == programa:
                can_receive = True
            elif role == "estudiante" and student_email is not None and email == student_email:
                can_receive = True

            if not can_receive:
                continue

            try:
                await websocket.send_json(payload)
            except Exception:
                stale_connections.append(websocket)

        for websocket in stale_connections:
            self.disconnect(websocket)


appointment_realtime_manager = AppointmentRealtimeManager()
